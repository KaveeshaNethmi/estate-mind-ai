from openai import OpenAI

from app.core.config import CHAT_MODEL, OPENAI_API_KEY
from app.services.conversation_service import (
    add_message,
    create_conversation,
    format_chat_history,
    get_conversation_messages,
    get_current_selection,
    get_focused_property,
    get_last_search_results,
    get_search_state,
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
from app.services.search_state_service import merge_search_state

client = OpenAI(api_key=OPENAI_API_KEY)


def build_pinecone_context(results: list[dict]) -> str:
    """
    Convert retrieved property results into context for the answer LLM.
    """

    context_parts: list[str] = []

    for result in results:
        property_data = result.get("property", {})

        context_parts.append(
            f"""
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
""".strip()
        )

    return "\n\n".join(context_parts)


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
    Generate an entity-aware conversational real-estate answer.

    A new search replaces the stored full search results.

    A follow-up reference reuses the stored results and updates only the
    current selection.
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

    print("FULL SEARCH RESULTS:", len(search_results))
    print("CURRENT SELECTION:", len(current_selection))
    print(
        "FOCUSED PROPERTY:",
        focused_property.get("property_id")
        if focused_property
        else None,
    )

    # ------------------------------------------------------------------
    # 2. Detect whether this is a new search or a property reference
    # ------------------------------------------------------------------

    entity_reference = detect_entity_reference(
        question=question,
        chat_history=chat_history,
        search_results=search_results,
        current_selection=current_selection,
        focused_property=focused_property,
    )

    print(
        "DETECTED ENTITY REFERENCE:",
        entity_reference.model_dump(),
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
            "Entity reference was detected, but no matching properties "
            "could be resolved:",
            entity_reference.model_dump(),
        )

    # ------------------------------------------------------------------
    # 4. Run a new retrieval only when previous results are not reused
    # ------------------------------------------------------------------

    if reused_previous_results:
        rewritten_query = question
        retrieved_results = referenced_results

        # Only update the conversational selection.
        # Do not overwrite the full search result set.
        save_current_selection(
            conversation_id=conversation_id,
            selected_results=retrieved_results,
        )

        updated_state = get_search_state(conversation_id)

    else:
        # Extract filters only for a new property search.
        extracted_filters = extract_filters_from_question(question)

        current_state = get_search_state(conversation_id)

        updated_state = merge_search_state(
            current_state=current_state,
            city=(
                city
                if city is not None
                else extracted_filters.city
            ),
            area=(
                area
                if area is not None
                else extracted_filters.area
            ),
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
                max_price
                if max_price is not None
                else extracted_filters.max_price
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

        retrieved_results = retrieve_properties_with_pinecone(
            query=rewritten_query,
            top_k=top_k,
            city=updated_state.get("city"),
            area=updated_state.get("area"),
            development=updated_state.get("development"),
            property_type=updated_state.get("property_type"),
            max_price=updated_state.get("max_price"),
            min_bedrooms=updated_state.get("min_bedrooms"),
        )

        # This is a genuine Pinecone search, so replace the full result
        # set and reset the conversational selection.
        save_last_search_results(
            conversation_id=conversation_id,
            retrieved_results=retrieved_results,
        )

    # ------------------------------------------------------------------
    # 5. Build context and generate the answer
    # ------------------------------------------------------------------

    context = build_pinecone_context(retrieved_results)

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful real estate AI copilot. "
                    "Answer only using the supplied property context. "
                    "Never invent property details."
                ),
            },
            {
                "role": "user",
                "content": f"""
Previous Conversation:
{chat_history}

Active Search State:
{updated_state}

Entity Reference:
{entity_reference.model_dump()}

Property Context:
{context}

Original User Question:
{question}

Instructions:
- Answer the original user question.
- Use only the supplied property context.
- When comparing properties, clearly label them by their displayed rank.
- Resolve pronouns and references using the entity-reference data.
- Do not invent property information.
- If the required information is unavailable, clearly say so.
""",
            },
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content

    if answer is None:
        answer = (
            "I do not have enough information to answer that question."
        )

    # ------------------------------------------------------------------
    # 6. Save conversation messages
    # ------------------------------------------------------------------

    add_message(
        conversation_id=conversation_id,
        role="user",
        content=question,
    )

    add_message(
        conversation_id=conversation_id,
        role="assistant",
        content=answer,
    )

    return {
        "conversation_id": conversation_id,
        "search_state": updated_state,
        "original_question": question,
        "rewritten_query": rewritten_query,
        "reference_detected": reference_detected,
        "reused_previous_results": reused_previous_results,
        "entity_reference": entity_reference.model_dump(),
        "answer": answer,
        "sources": retrieved_results,
    }