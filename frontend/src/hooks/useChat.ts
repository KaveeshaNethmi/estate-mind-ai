import { useRef, useState } from "react";
import { streamChat } from "../services/chatApi";
import type {
  ChatMessage,
  SearchState,
} from "../types/chat";

function createMessageId() {
  return crypto.randomUUID();
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] =
    useState<string | null>(null);

  const [searchState, setSearchState] =
    useState<SearchState>({});

  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const abortControllerRef =
    useRef<AbortController | null>(null);

  const sendMessage = async (question: string) => {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || isStreaming) {
      return;
    }

    const userMessage: ChatMessage = {
      id: createMessageId(),
      role: "user",
      content: trimmedQuestion,
    };

    const assistantMessageId = createMessageId();

    const assistantMessage: ChatMessage = {
      id: assistantMessageId,
      role: "assistant",
      content: "",
      isStreaming: true,
    };

    setMessages((currentMessages) => [
      ...currentMessages,
      userMessage,
      assistantMessage,
    ]);

    setError(null);
    setIsStreaming(true);

    const controller = new AbortController();
    abortControllerRef.current = controller;

    try {
      for await (const event of streamChat(
        {
          question: trimmedQuestion,
          top_k: 5,
          conversation_id: conversationId,
        },
        controller.signal,
      )) {
        switch (event.type) {
          case "metadata": {
            setConversationId(
              event.data.conversation_id,
            );

            setSearchState(event.data.search_state);

            break;
          }

          case "token": {
            setMessages((currentMessages) =>
              currentMessages.map((message) =>
                message.id === assistantMessageId
                  ? {
                      ...message,
                      content:
                        message.content +
                        event.data.content,
                    }
                  : message,
              ),
            );

            break;
          }

          case "complete": {
            setMessages((currentMessages) =>
              currentMessages.map((message) =>
                message.id === assistantMessageId
                  ? {
                      ...message,

                      // Important:
                      // Replace streamed text with backend's
                      // final citation-cleaned answer.
                      content: event.data.answer,

                      isStreaming: false,
                      citations: event.data.citations,
                      confidence: event.data.confidence,
                      sources: event.data.sources,
                    }
                  : message,
              ),
            );

            break;
          }

          case "error": {
            throw new Error(
              event.data.message ||
                "The response could not be generated.",
            );
          }
        }
      }
    } catch (caughtError) {
      if (
        caughtError instanceof DOMException &&
        caughtError.name === "AbortError"
      ) {
        setMessages((currentMessages) =>
          currentMessages.map((message) =>
            message.id === assistantMessageId
              ? {
                  ...message,
                  isStreaming: false,
                }
              : message,
          ),
        );

        return;
      }

      const message =
        caughtError instanceof Error
          ? caughtError.message
          : "Something went wrong while generating the response.";

      setError(message);

      setMessages((currentMessages) =>
        currentMessages.map((chatMessage) =>
          chatMessage.id === assistantMessageId
            ? {
                ...chatMessage,
                content:
                  chatMessage.content ||
                  "Sorry, I couldn't generate a response. Please try again.",
                isStreaming: false,
              }
            : chatMessage,
        ),
      );
    } finally {
      setIsStreaming(false);
      abortControllerRef.current = null;
    }
  };

  const stopGeneration = () => {
    abortControllerRef.current?.abort();
  };

  const resetConversation = () => {
    abortControllerRef.current?.abort();

    setMessages([]);
    setConversationId(null);
    setSearchState({});
    setError(null);
    setIsStreaming(false);
  };

  return {
    messages,
    conversationId,
    searchState,
    isStreaming,
    error,

    sendMessage,
    stopGeneration,
    resetConversation,
  };
}