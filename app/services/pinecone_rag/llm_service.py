from typing import AsyncGenerator

from openai import OpenAI

from app.core.config import CHAT_MODEL, OPENAI_API_KEY
from app.schemas.chat_schema import PreparedChatResponse
from app.services.citation_service import (
    add_citation_ids,
    build_citation_context,
    extract_citations,
    remove_invalid_citations,
)
from app.services.confidence_service import calculate_confidence
from app.services.conversation_service import (
    add_message,
    create_conversation,
    format_chat_history,
    get_conversation_messages,
    get_current_selection,
    get_focused_property,
    get_last_search_results,
    get_search_state,
    save_conversation_messages,
    save_current_selection,
    save_last_search_results,
    update_search_state,
)
from app.services.entity_reference_service import (
    detect_entity_reference,
    resolve_entity_reference,
)
from app.services.filter_extraction_service import (
    extract_filters_from_question,
)
from app.services.pinecone_rag.retrieval_service import (
    retrieve_properties_with_pinecone,
)
from app.services.query_rewriting_service import rewrite_query
from app.services.reranking_service import rerank_properties
from app.services.search_state_service import merge_search_state
from app.services.streaming_service import format_sse_event

from openai.types.chat import (
    ChatCompletionMessageParam,
)

client = OpenAI(api_key=OPENAI_API_KEY)


def build_pinecone_context(results: list[dict]) -> str:
    """
    Convert retrieved property results into context for the answer LLM.
    """

    context_parts: list[str] = []

    for result in results:
        property_data = result.get("property", {})

        context_parts.append(f"""
Property {result.get("rank")}:
Property ID: {property_data.get("property_id")}
Name: {property_data.get("property_name")}
City: {property_data.get("city")}
Area: {property_data.get("area")}
Development: {property_data.get("development")}
Type: {property_data.get("property_type")}
Price: {property_data.get("price")}
Bedrooms: {property_data.get("bedrooms")}
Bathrooms: {property_data.get("bathrooms")}
Rental Yield: {property_data.get("rental_yield")}
ROI: {property_data.get("roi_15")}

Details:
{property_data.get("semantic_text")}
""".strip())

    return "\n\n".join(context_parts)


def build_answer_messages(
    prepared: PreparedChatResponse,
) -> list[ChatCompletionMessageParam]:
    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": (
                "You are a helpful real estate AI copilot. "
                "Answer only using the supplied property sources. "
                "Every factual claim about a property must include "
                "the relevant citation in square brackets, such as "
                "[1]. An answer about properties without citations "
                "is invalid. Never invent property details or "
                "citation numbers."
            ),
        },
        {
            "role": "user",
            "content": f"""
Previous Conversation:
{prepared.chat_history}

Active Search State:
{prepared.search_state}

Entity Reference:
{prepared.entity_reference}

Property Sources:
{prepared.context}

Original User Question:
{prepared.question}

Instructions:
- Answer the original user question directly.
- Use only the supplied property sources.
- Cite every property-specific statement.
- Use only citation numbers shown in the property sources.
- Place citations immediately after the supported statement.
- When several sources support one statement, cite each source.
- When comparing properties, cite every property involved.
- Do not invent property information.
- If the required information is unavailable, clearly say so.
""",
        },
    ]

    return messages


async def stream_property_answer(
    prepared: PreparedChatResponse,
) -> AsyncGenerator[str, None]:
    yield format_sse_event(
        event="metadata",
        data={
            "conversation_id": (prepared.conversation_id),
            "rewritten_query": (prepared.rewritten_query),
            "search_state": (prepared.search_state),
            "reference_detected": (prepared.reference_detected),
            "reused_previous_results": (prepared.reused_previous_results),
        },
    )

    full_answer_parts: list[str] = []

    try:
        stream = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=build_answer_messages(prepared),
            temperature=0.2,
            stream=True,
        )

        for chunk in stream:
            token = chunk.choices[0].delta.content

            if not token:
                continue

            full_answer_parts.append(token)

            yield format_sse_event(
                event="token",
                data={"content": token},
            )

        full_answer = "".join(full_answer_parts)

        if not full_answer:
            full_answer = "I do not have enough information " "to answer that question."

        full_answer = remove_invalid_citations(
            answer=full_answer,
            results=prepared.retrieved_results,
        )

        citations = extract_citations(
            answer=full_answer,
            results=prepared.retrieved_results,
        )

        confidence = calculate_confidence(
            results=prepared.retrieved_results,
            citations=citations,
        )

        add_message(
            conversation_id=(prepared.conversation_id),
            role="user",
            content=prepared.question,
        )

        add_message(
            conversation_id=(prepared.conversation_id),
            role="assistant",
            content=full_answer,
        )

        yield format_sse_event(
            event="complete",
            data={
                "answer": full_answer,
                "citations": citations,
                "confidence": confidence,
                "sources": (prepared.retrieved_results),
            },
        )

    except Exception as exc:
        yield format_sse_event(
            event="error",
            data={
                "message": ("The response could not be " "generated."),
                "details": str(exc),
            },
        )


def prepare_chat_response(
    question: str,
    top_k: int = 5,
    conversation_id: str | None = None,
    city: str | None = None,
    area: str | None = None,
    development: str | None = None,
    property_type: str | None = None,
    max_price: float | None = None,
    min_bedrooms: int | None = None,
) -> PreparedChatResponse:
    """
    Prepare an entity-aware conversational real-estate response.

    This function:
    - creates or loads the conversation
    - loads previous messages and retrieval state
    - detects and resolves property references
    - extracts and merges search filters
    - rewrites the query
    - retrieves and reranks properties
    - saves retrieval state
    - assigns citation IDs
    - builds the property context

    It does not generate or save the final assistant answer.
    """

    if not conversation_id:
        conversation_id = create_conversation()

    # ------------------------------------------------------------------
    # 1. Load conversation state
    # ------------------------------------------------------------------

    previous_messages = get_conversation_messages(conversation_id)

    chat_history = format_chat_history(previous_messages)

    search_results = get_last_search_results(conversation_id)

    current_selection = get_current_selection(conversation_id)

    focused_property = get_focused_property(conversation_id)

    # ------------------------------------------------------------------
    # 2. Detect whether this is a new search or property reference
    # ------------------------------------------------------------------

    entity_reference = detect_entity_reference(
        question=question,
        chat_history=chat_history,
        search_results=search_results,
        current_selection=current_selection,
        focused_property=focused_property,
    )

    reference_detected = entity_reference.uses_previous_results

    # ------------------------------------------------------------------
    # 3. Resolve previous properties when this is a follow-up
    # ------------------------------------------------------------------

    referenced_results: list[dict] = []

    if reference_detected:
        referenced_results = resolve_entity_reference(
            reference=entity_reference,
            search_results=search_results,
            current_selection=current_selection,
            focused_property=focused_property,
        )

    reused_previous_results = bool(referenced_results)

    if reference_detected and not referenced_results:
        print(
            "Entity reference was detected, but no matching "
            "properties could be resolved:",
            entity_reference.model_dump(),
        )

    final_results: list[dict]

    # ------------------------------------------------------------------
    # 4. Reuse previous results or perform a new search
    # ------------------------------------------------------------------

    if reused_previous_results:
        rewritten_query = question
        final_results = referenced_results

        save_current_selection(
            conversation_id=conversation_id,
            selected_results=final_results,
        )

        updated_state = get_search_state(conversation_id)

    else:
        extracted_filters = extract_filters_from_question(question)

        current_state = get_search_state(conversation_id)

        updated_state = merge_search_state(
            current_state=current_state,
            city=(city if city is not None else extracted_filters.city),
            area=(area if area is not None else extracted_filters.area),
            development=(
                development
                if development is not None
                else extracted_filters.development
            ),
            property_type=(
                property_type
                if property_type is not None
                else extracted_filters.property_type
            ),
            max_price=(
                max_price if max_price is not None else extracted_filters.max_price
            ),
            min_bedrooms=(
                min_bedrooms
                if min_bedrooms is not None
                else extracted_filters.min_bedrooms
            ),
        )

        update_search_state(
            conversation_id=conversation_id,
            new_state=updated_state,
        )

        rewritten_query = rewrite_query(
            question=question,
            chat_history=chat_history,
            search_state=updated_state,
        )

        candidate_count = max(
            top_k * 3,
            15,
        )

        pinecone_results = retrieve_properties_with_pinecone(
            query=rewritten_query,
            top_k=candidate_count,
            city=updated_state.get("city"),
            area=updated_state.get("area"),
            development=updated_state.get("development"),
            property_type=updated_state.get("property_type"),
            max_price=updated_state.get("max_price"),
            min_bedrooms=updated_state.get("min_bedrooms"),
        )

        final_results = rerank_properties(
            question=question,
            results=pinecone_results,
            top_n=top_k,
        )

        save_last_search_results(
            conversation_id=conversation_id,
            retrieved_results=final_results,
        )

    # ------------------------------------------------------------------
    # 5. Add citations and build context
    # ------------------------------------------------------------------

    cited_results = add_citation_ids(final_results)

    context = build_citation_context(cited_results)

    # ------------------------------------------------------------------
    # 6. Return prepared data
    # ------------------------------------------------------------------

    return PreparedChatResponse(
        conversation_id=conversation_id,
        question=question,
        rewritten_query=rewritten_query,
        chat_history=chat_history,
        search_state=updated_state,
        retrieved_results=cited_results,
        context=context,
        reference_detected=reference_detected,
        reused_previous_results=reused_previous_results,
        entity_reference=entity_reference.model_dump(),
    )


def generate_pinecone_answer(
    question: str,
    top_k: int = 5,
    conversation_id: str | None = None,
    city: str | None = None,
    area: str | None = None,
    development: str | None = None,
    property_type: str | None = None,
    max_price: float | None = None,
    min_bedrooms: int | None = None,
) -> dict:
    """
    Generate a non-streaming entity-aware conversational
    real-estate answer.
    """

    prepared = prepare_chat_response(
        question=question,
        top_k=top_k,
        conversation_id=conversation_id,
        city=city,
        area=area,
        development=development,
        property_type=property_type,
        max_price=max_price,
        min_bedrooms=min_bedrooms,
    )

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=build_answer_messages(prepared),
        temperature=0.2,
    )

    answer = response.choices[0].message.content

    if answer is None:
        answer = "I do not have enough information to answer " "that question."

    answer = remove_invalid_citations(
        answer=answer,
        results=prepared.retrieved_results,
    )

    citations = extract_citations(
        answer=answer,
        results=prepared.retrieved_results,
    )

    confidence = calculate_confidence(
        results=prepared.retrieved_results,
        citations=citations,
    )

    add_message(
        conversation_id=prepared.conversation_id,
        role="user",
        content=prepared.question,
    )

    add_message(
        conversation_id=prepared.conversation_id,
        role="assistant",
        content=answer,
    )

    return {
        "conversation_id": (prepared.conversation_id),
        "search_state": prepared.search_state,
        "original_question": prepared.question,
        "rewritten_query": (prepared.rewritten_query),
        "reference_detected": (prepared.reference_detected),
        "reused_previous_results": (prepared.reused_previous_results),
        "entity_reference": (prepared.entity_reference),
        "answer": answer,
        "citations": citations,
        "confidence": confidence,
        "sources": prepared.retrieved_results,
    }
