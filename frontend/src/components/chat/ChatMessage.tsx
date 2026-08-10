import { Bot, UserRound } from "lucide-react";
import type { ChatMessage as ChatMessageType } from "../../types/chat";

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({
  message,
}: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <article
      className={[
        "flex gap-3",
        isUser ? "justify-end" : "justify-start",
      ].join(" ")}
    >
      {!isUser && (
        <div
          className="
            flex size-8 shrink-0 items-center justify-center
            rounded-control bg-primary-light text-primary
          "
        >
          <Bot size={16} />
        </div>
      )}

      <div
        className={[
          "max-w-[85%] rounded-card px-4 py-3 sm:max-w-[75%]",
          isUser
            ? "bg-primary text-text-inverse"
            : "bg-surface shadow-card",
        ].join(" ")}
      >
        <p className="whitespace-pre-wrap text-sm leading-6">
          {message.content}

          {message.isStreaming && (
            <span className="ml-1 inline-block animate-pulse">
              ▍
            </span>
          )}
        </p>

        {!isUser &&
          !message.isStreaming &&
          message.confidence !== undefined && (
            <div className="mt-3 flex items-center gap-2 text-xs text-text-muted">
              <span>
                Confidence{" "}
                {Math.round(message.confidence * 100)}%
              </span>
            </div>
          )}
      </div>

      {isUser && (
        <div
          className="
            flex size-8 shrink-0 items-center justify-center
            rounded-control bg-surface-strong text-text-secondary
          "
        >
          <UserRound size={16} />
        </div>
      )}
    </article>
  );
}