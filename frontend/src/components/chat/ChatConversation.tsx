import { useEffect, useRef } from "react";
import type { ChatMessage as ChatMessageType } from "../../types/chat";
import { ChatMessage } from "./ChatMessage";

interface ChatConversationProps {
  messages: ChatMessageType[];
}

export function ChatConversation({
  messages,
}: ChatConversationProps) {
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [messages]);

  return (
    <div className="mx-auto w-full max-w-3xl space-y-5 px-4 py-6 sm:px-6">
      {messages.map((message) => (
        <ChatMessage
          key={message.id}
          message={message}
        />
      ))}

      <div ref={bottomRef} />
    </div>
  );
}