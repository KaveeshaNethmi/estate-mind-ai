from datetime import datetime, timezone
from gc import collect

from bson import ObjectId

from app.core.database import get_conversations_collection


def create_conversation() -> str:
    collection = get_conversations_collection()
    print("collection", collection)

    result = collection.insert_one(
        {
            "messages": [],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
    )
    print("result", result)

    return str(result.inserted_id)


def get_conversation_messages(conversation_id: str, limit: int = 6) -> list[dict]:
    if not conversation_id:
        return []

    collection = get_conversations_collection()

    conversation = collection.find_one({"_id": ObjectId(conversation_id)})

    if not conversation:
        return []

    messages = conversation.get("messages", [])

    return messages[-limit:]


def add_message(conversation_id: str, role: str, content: str):
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
            }
        },
    )


def format_chat_history(messages: list[dict]) -> str:
    if not messages:
        return "No previous conversation."

    formatted = []

    for message in messages:
        role = message.get("role", "unknown")
        content = message.get("content", "")

        formatted.append(f"{role.upper()}: {content}")

    return "|\n".join(formatted)
