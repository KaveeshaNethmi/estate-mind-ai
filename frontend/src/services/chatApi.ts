import type {
  ChatErrorData,
  ChatMetadata,
  ChatRequest,
  ChatStreamEvent,
  ChatCompleteData,
} from "../types/chat";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE_URL) {
  throw new Error(
    "VITE_API_BASE_URL is not configured. Add it to frontend/.env.",
  );
}

function parseEvent(
  eventName: string,
  data: string,
): ChatStreamEvent | null {
  if (!data) {
    return null;
  }

  const parsedData: unknown = JSON.parse(data);

  switch (eventName) {
    case "metadata":
      return {
        type: "metadata",
        data: parsedData as ChatMetadata,
      };

    case "token":
      return {
        type: "token",
        data: parsedData as { content: string },
      };

    case "complete":
      return {
        type: "complete",
        data: parsedData as ChatCompleteData,
      };

    case "error":
      return {
        type: "error",
        data: parsedData as ChatErrorData,
      };

    default:
      return null;
  }
}

export async function* streamChat(
  request: ChatRequest,
  signal?: AbortSignal,
): AsyncGenerator<ChatStreamEvent> {
  const response = await fetch(`${API_BASE_URL}/chat/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    },
    body: JSON.stringify(request),
    signal,
  });

  if (!response.ok) {
    const responseBody = await response.text();

    throw new Error(
      responseBody ||
        `Chat request failed with status ${response.status}.`,
    );
  }

  if (!response.body) {
    throw new Error("The chat response does not contain a stream.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  let buffer = "";

  try {
    while (true) {
      const { done, value } = await reader.read();

      if (done) {
        break;
      }

      buffer += decoder.decode(value, {
        stream: true,
      });

      const events = buffer.split("\n\n");

      // Keep the last possibly-incomplete event in the buffer.
      buffer = events.pop() ?? "";

      for (const rawEvent of events) {
        if (!rawEvent.trim()) {
          continue;
        }

        const lines = rawEvent.split("\n");

        let eventName = "";
        const dataLines: string[] = [];

        for (const line of lines) {
          if (line.startsWith("event:")) {
            eventName = line.slice("event:".length).trim();
          }

          if (line.startsWith("data:")) {
            dataLines.push(
              line.slice("data:".length).trim(),
            );
          }
        }

        if (!eventName || dataLines.length === 0) {
          continue;
        }

        const event = parseEvent(
          eventName,
          dataLines.join("\n"),
        );

        if (event) {
          yield event;
        }
      }
    }

    // Handle a final event if the stream ends without
    // another blank line.
    if (buffer.trim()) {
      const lines = buffer.split("\n");

      let eventName = "";
      const dataLines: string[] = [];

      for (const line of lines) {
        if (line.startsWith("event:")) {
          eventName = line.slice("event:".length).trim();
        }

        if (line.startsWith("data:")) {
          dataLines.push(
            line.slice("data:".length).trim(),
          );
        }
      }

      if (eventName && dataLines.length > 0) {
        const event = parseEvent(
          eventName,
          dataLines.join("\n"),
        );

        if (event) {
          yield event;
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}