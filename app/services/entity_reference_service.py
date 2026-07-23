from decimal import Decimal
import re
from typing import TypeAlias

from openai import OpenAI

from app.core.config import CHAT_MODEL, OPENAI_API_KEY
from app.schemas.entity_reference_schema import EntityReference

client = OpenAI(api_key=OPENAI_API_KEY)

NumericValue: TypeAlias = int | float | str | Decimal

ORDINAL_RANKS = {
    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5,
}

NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
}


def format_previous_properties(properties: list[dict]) -> str:
    """
    Create a compact representation of previous properties for
    entity-reference classification.
    """

    if not properties:
        return "No previous properties are available."

    formatted_properties: list[str] = []

    for property_data in properties:
        formatted_properties.append(
            (
                f"Rank: {property_data.get('rank')}\n"
                f"Property ID: {property_data.get('property_id')}\n"
                f"Name: {property_data.get('property_name')}\n"
                f"Development: {property_data.get('development')}\n"
                f"Price: {property_data.get('price')}\n"
                f"Rental Yield: {property_data.get('rental_yield')}\n"
                f"ROI: {property_data.get('roi_15')}"
            )
        )

    return "\n\n".join(formatted_properties)


def detect_entity_reference(
    question: str,
    chat_history: str,
    search_results: list[dict],
    current_selection: list[dict] | None = None,
    focused_property: dict | None = None,
) -> EntityReference:
    """
    Classify how the current question should use conversation property state.

    search_results:
        Full result set from the latest Pinecone search.

    current_selection:
        The subset currently being discussed.

    focused_property:
        A single property selected by the previous turn.
    """

    current_selection = current_selection or []

    deterministic_reference = detect_deterministic_reference(
        question=question,
        search_results=search_results,
        current_selection=current_selection,
        focused_property=focused_property,
    )

    if deterministic_reference is not None:
        return deterministic_reference

    if not search_results and not current_selection and not focused_property:
        return EntityReference()

    previous_property_text = format_previous_properties(search_results)
    current_selection_text = format_previous_properties(current_selection)
    focused_property_text = format_previous_properties(
        [focused_property] if focused_property else []
    )

    completion = client.beta.chat.completions.parse(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Classify how a real-estate follow-up question should use "
                    "properties from the conversation. Do not answer the "
                    "question. Return only the structured classification."
                ),
            },
            {
                "role": "user",
                "content": f"""
Classify the current user question.

Available actions:

1. new_search
Use when the user asks for new or different properties, changes a location,
budget, property type, bedroom requirement, or otherwise requires retrieval.

2. select_by_rank
Use for explicit ranks from the full latest search results.
Examples:
- first property
- first two
- second and third
- top three

3. select_from_current
Use for operations over the currently selected properties.
Examples:
- which is cheaper?
- which has the best rental yield?
- compare them
- which has the highest ROI?

4. use_focused
Use when a singular pronoun refers to the focused property.
Examples:
- what is its ROI?
- is it furnished?
- tell me more about it

Operation rules:
- cheaper or cheapest -> cheapest
- most expensive -> most_expensive
- best or highest rental yield -> highest_rental_yield
- lowest rental yield -> lowest_rental_yield
- best or highest ROI -> highest_roi
- lowest ROI -> lowest_roi
- otherwise -> none

Additional rules:
- Explicit ranks always use action = select_by_rank.
- Comparative questions without explicit ranks use
  action = select_from_current.
- Singular references such as "it" and "its" use use_focused only when
  a focused property exists.
- Do not invent property names or ranks.
- Set uses_previous_results to true for every action except new_search.

Previous conversation:
{chat_history}

Full latest search results:
{previous_property_text}

Current selection:
{current_selection_text}

Focused property:
{focused_property_text}

Current question:
{question}
""",
            },
        ],
        response_format=EntityReference,
        temperature=0,
    )

    parsed = completion.choices[0].message.parsed

    if parsed is None:
        return EntityReference()

    return normalize_entity_reference(parsed)


def detect_deterministic_reference(
    question: str,
    search_results: list[dict],
    current_selection: list[dict],
    focused_property: dict | None,
) -> EntityReference | None:
    """
    Resolve common and predictable references without an LLM.
    """

    normalized_question = question.lower().strip()

    # Examples:
    # first two
    # top three
    # first 3
    first_n_match = re.search(
        r"\b(?:the\s+)?(?:first|top)\s+"
        r"(one|two|three|four|five|\d+)\b",
        normalized_question,
    )

    if first_n_match and search_results:
        number_text = first_n_match.group(1)
        count = (
            int(number_text)
            if number_text.isdigit()
            else NUMBER_WORDS[number_text]
        )

        count = min(count, len(search_results))

        return EntityReference(
            uses_previous_results=True,
            action="select_by_rank",
            ranks=list(range(1, count + 1)),
            operation="none",
        )

    # Examples:
    # first and second
    # first, second and third
    mentioned_ranks = [
        rank
        for ordinal, rank in ORDINAL_RANKS.items()
        if re.search(rf"\b{ordinal}\b", normalized_question)
    ]

    if len(mentioned_ranks) > 1 and search_results:
        valid_ranks = [
            rank
            for rank in sorted(set(mentioned_ranks))
            if rank <= len(search_results)
        ]

        return EntityReference(
            uses_previous_results=True,
            action="select_by_rank",
            ranks=valid_ranks,
            operation="none",
        )

    # Examples:
    # first one
    # second property
    # third apartment
    for ordinal, rank in ORDINAL_RANKS.items():
        if (
            search_results
            and rank <= len(search_results)
            and re.search(
                rf"\b(?:the\s+)?{ordinal}"
                rf"(?:\s+one|\s+property|\s+apartment|\s+villa)?\b",
                normalized_question,
            )
        ):
            return EntityReference(
                uses_previous_results=True,
                action="select_by_rank",
                ranks=[rank],
                operation="none",
            )

    if _contains_any(
        normalized_question,
        [
            "cheaper one",
            "cheapest one",
            "which is cheaper",
            "which one is cheaper",
            "least expensive",
            "lowest priced",
        ],
    ):
        return EntityReference(
            uses_previous_results=True,
            action="select_from_current",
            operation="cheapest",
        )

    if _contains_any(
        normalized_question,
        [
            "most expensive",
            "highest priced",
        ],
    ):
        return EntityReference(
            uses_previous_results=True,
            action="select_from_current",
            operation="most_expensive",
        )

    if _contains_any(
        normalized_question,
        [
            "highest rental yield",
            "best rental yield",
            "which has the best yield",
            "which one has the best yield",
        ],
    ):
        return EntityReference(
            uses_previous_results=True,
            action="select_from_current",
            operation="highest_rental_yield",
        )

    if _contains_any(
        normalized_question,
        [
            "lowest rental yield",
            "worst rental yield",
        ],
    ):
        return EntityReference(
            uses_previous_results=True,
            action="select_from_current",
            operation="lowest_rental_yield",
        )

    if _contains_any(
        normalized_question,
        [
            "highest roi",
            "best roi",
            "which has the best roi",
        ],
    ):
        return EntityReference(
            uses_previous_results=True,
            action="select_from_current",
            operation="highest_roi",
        )

    if "lowest roi" in normalized_question:
        return EntityReference(
            uses_previous_results=True,
            action="select_from_current",
            operation="lowest_roi",
        )

    if _contains_any(
        normalized_question,
        [
            "compare them",
            "compare those",
            "compare these",
            "all of them",
            "those properties",
            "these properties",
        ],
    ):
        return EntityReference(
            uses_previous_results=True,
            action="select_from_current",
            operation="none",
        )

    if focused_property and re.search(
        r"\b(it|its|that one|that property|this one|this property)\b",
        normalized_question,
    ):
        return EntityReference(
            uses_previous_results=True,
            action="use_focused",
            operation="none",
        )

    return None


def resolve_entity_reference(
    reference: EntityReference,
    search_results: list[dict],
    current_selection: list[dict],
    focused_property: dict | None,
) -> list[dict]:
    """
    Resolve the classified reference into retrieval-result objects.
    """

    if not reference.uses_previous_results:
        return []

    if reference.action == "select_by_rank":
        source_properties = search_results

        requested_ranks = set(reference.ranks)

        selected = [
            property_data
            for property_data in source_properties
            if property_data.get("rank") in requested_ranks
        ]

    elif reference.action == "select_from_current":
        source_properties = current_selection or search_results

        if reference.operation == "none":
            selected = source_properties
        else:
            selected_property = select_property_by_operation(
                properties=source_properties,
                operation=reference.operation,
            )

            selected = (
                [selected_property]
                if selected_property is not None
                else []
            )

    elif reference.action == "use_focused":
        selected = [focused_property] if focused_property else []

    else:
        selected = []

    return [
        to_retrieval_result(
            property_data=property_data,
            rank=index + 1,
        )
        for index, property_data in enumerate(selected)
    ]


def select_property_by_operation(
    properties: list[dict],
    operation: str,
) -> dict | None:
    operation_config = {
        "cheapest": ("price", False),
        "most_expensive": ("price", True),
        "highest_rental_yield": ("rental_yield", True),
        "lowest_rental_yield": ("rental_yield", False),
        "highest_roi": ("roi_15", True),
        "lowest_roi": ("roi_15", False),
    }

    config = operation_config.get(operation)

    if config is None:
        return None

    field_name, choose_max = config

    return _select_numeric_property(
        properties=properties,
        field_name=field_name,
        choose_max=choose_max,
    )


def to_retrieval_result(
    property_data: dict,
    rank: int,
) -> dict:
    """
    Convert a stored property into the retrieval-result structure
    expected by the answer-generation pipeline.
    """

    property_metadata = {
        key: value
        for key, value in property_data.items()
        if key not in {"rank", "score"}
    }

    return {
        "rank": rank,
        "score": property_data.get("score"),
        "property": property_metadata,
    }


def normalize_entity_reference(
    reference: EntityReference,
) -> EntityReference:
    """
    Prevent contradictory structured output from the model.
    """

    if reference.action == "new_search":
        reference.uses_previous_results = False
        reference.ranks = []
        reference.operation = "none"
        reference.property_name = None
        return reference

    reference.uses_previous_results = True

    if reference.action != "select_by_rank":
        reference.ranks = []

    if reference.action != "select_from_current":
        reference.operation = "none"

    return reference


def _select_numeric_property(
    properties: list[dict],
    field_name: str,
    choose_max: bool,
) -> dict | None:
    valid_properties: list[tuple[dict, float]] = []

    for property_data in properties:
        numeric_value = _to_float(property_data.get(field_name))

        if numeric_value is not None:
            valid_properties.append(
                (property_data, numeric_value)
            )

    if not valid_properties:
        return None

    selected_property, _ = (
        max(valid_properties, key=lambda item: item[1])
        if choose_max
        else min(valid_properties, key=lambda item: item[1])
    )

    return selected_property


def _to_float(
    value: NumericValue | None,
) -> float | None:
    if value is None or value == "":
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _contains_any(
    text: str,
    phrases: list[str],
) -> bool:
    return any(phrase in text for phrase in phrases)