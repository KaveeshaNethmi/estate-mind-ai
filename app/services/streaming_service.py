import json
from typing import Any, AsyncGenerator


def format_sse_event(event: str, data: dict[str, Any]) -> str:
    """
    Convert an event and its payload into Server-Sent Events format.
    """

    serialized_data = json.dumps(data, default=str, ensure_ascii=False)

    return f"event: {event}\ndata: {serialized_data}\n\n"


async def stream_error(message: str) -> AsyncGenerator[str, None]:
    yield format_sse_event(event="error", data={"message": message})
