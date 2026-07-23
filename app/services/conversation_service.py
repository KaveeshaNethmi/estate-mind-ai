from datetime import datetime, timezone

from bson import ObjectId

from app.core.database import get_conversations_collection


def create_conversation() -> str:
    collection = get_conversations_collection()
    now = datetime.now(timezone.utc)

    result = collection.insert_one(
        {
            "messages": [],
            "search_state": {
                "city": None,
                "area": None,
                "development": None,
                "property_type": None,
                "max_price": None,
                "min_bedrooms": None,
            },
            "last_search_results": [],
            "current_selection": [],
            "focused_property": None,
            "created_at": now,
            "updated_at": now,
        }
    )

    return str(result.inserted_id)


def get_conversation(
    conversation_id: str,
) -> dict | None:
    if not conversation_id:
        return None

    try:
        object_id = ObjectId(conversation_id)
    except Exception:
        return None

    collection = get_conversations_collection()

    return collection.find_one({"_id": object_id})


def get_conversation_messages(
    conversation_id: str,
    limit: int = 6,
) -> list[dict]:
    conversation = get_conversation(conversation_id)

    if not conversation:
        return []

    messages = conversation.get("messages", [])

    return messages[-limit:]


def add_message(
    conversation_id: str,
    role: str,
    content: str,
) -> None:
    collection = get_conversations_collection()

    collection.update_one(
        {"_id": ObjectId(conversation_id)},
        {
            "$push": {
                "messages": {
                    "role": role,
                    "content": content,
                    "created_at": datetime.now(timezone.utc),
                }
            },
            "$set": {
                "updated_at": datetime.now(timezone.utc),
            },
        },
    )


def format_chat_history(
    messages: list[dict],
) -> str:
    if not messages:
        return "No previous conversation."

    formatted_messages: list[str] = []

    for message in messages:
        role = message.get("role", "unknown")
        content = message.get("content", "")

        formatted_messages.append(
            f"{role.upper()}: {content}"
        )

    return "\n".join(formatted_messages)


def get_search_state(
    conversation_id: str,
) -> dict:
    conversation = get_conversation(conversation_id)

    if not conversation:
        return {}

    return conversation.get("search_state", {})


def update_search_state(
    conversation_id: str,
    new_state: dict,
) -> None:
    collection = get_conversations_collection()

    collection.update_one(
        {"_id": ObjectId(conversation_id)},
        {
            "$set": {
                "search_state": new_state,
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )


def serialize_retrieved_properties(
    retrieved_results: list[dict],
) -> list[dict]:
    """
    Convert Pinecone retrieval results into the structure stored
    inside the conversation document.
    """

    stored_properties: list[dict] = []

    for result in retrieved_results:
        property_data = result.get("property", {})

        stored_properties.append(
            {
                "rank": result.get("rank"),
                "score": result.get("score"),
                "property_id": property_data.get("property_id"),
                "property_name": property_data.get("property_name"),
                "city": property_data.get("city"),
                "area": property_data.get("area"),
                "development": property_data.get("development"),
                "property_type": property_data.get("property_type"),
                "price": property_data.get("price"),
                "bedrooms": property_data.get("bedrooms"),
                "bathrooms": property_data.get("bathrooms"),
                "rental_yield": property_data.get("rental_yield"),
                "roi_15": property_data.get("roi_15"),
                "semantic_text": property_data.get("semantic_text"),
            }
        )

    return stored_properties


def save_last_search_results(
    conversation_id: str,
    retrieved_results: list[dict],
) -> None:
    """
    Save a new Pinecone search result set.

    A genuine new search:
    - replaces last_search_results
    - resets current_selection to the full result set
    - clears focused_property
    """

    collection = get_conversations_collection()

    stored_properties = serialize_retrieved_properties(
        retrieved_results
    )

    collection.update_one(
        {"_id": ObjectId(conversation_id)},
        {
            "$set": {
                "last_search_results": stored_properties,
                "current_selection": stored_properties,
                "focused_property": None,
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )


def get_last_search_results(
    conversation_id: str,
) -> list[dict]:
    conversation = get_conversation(conversation_id)

    if not conversation:
        return []

    return conversation.get("last_search_results", [])


def save_current_selection(
    conversation_id: str,
    selected_results: list[dict],
) -> None:
    """
    Update only the subset currently being discussed.

    This must not overwrite last_search_results.
    """

    collection = get_conversations_collection()

    stored_properties = serialize_retrieved_properties(
        selected_results
    )

    focused_property = (
        stored_properties[0]
        if len(stored_properties) == 1
        else None
    )

    collection.update_one(
        {"_id": ObjectId(conversation_id)},
        {
            "$set": {
                "current_selection": stored_properties,
                "focused_property": focused_property,
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )


def get_current_selection(
    conversation_id: str,
) -> list[dict]:
    conversation = get_conversation(conversation_id)

    if not conversation:
        return []

    current_selection = conversation.get(
        "current_selection",
        [],
    )

    if current_selection:
        return current_selection

    # Fallback for older conversations that do not yet have
    # current_selection.
    return conversation.get("last_search_results", [])


def get_focused_property(
    conversation_id: str,
) -> dict | None:
    conversation = get_conversation(conversation_id)

    if not conversation:
        return None

    return conversation.get("focused_property")