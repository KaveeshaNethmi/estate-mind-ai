import { ArrowUp, MapPin, Paperclip, SlidersHorizontal } from "lucide-react";
import { useState } from "react";

interface ChatInputProps {
  onSubmit?: (message: string) => void;
  disabled?: boolean;
}

export const ChatInput = ({ onSubmit, disabled = false }: ChatInputProps) => {
  const [message, setMessage] = useState("");

  const trimmedMessage = message.trim();
  const canSubmit = trimmedMessage.length > 0 && !disabled;

  const handleSubmit = () => {
    const trimmedMessage = message.trim();

    if (!trimmedMessage || disabled) {
      return;
    }

    onSubmit?.(trimmedMessage);
    setMessage("");
  };
  
  const secondaryButtonClass =
    "focus-ring flex size-10 shrink-0 items-center justify-center rounded-control text-text-muted transition-colors hover:bg-surface-subtle hover:text-text-primary";

  return (
    <div className="rounded-panel border border-border bg-surface p-2 shadow-input">
      <div className="flex items-center gap-2">
        <button
          type="button"
          className={secondaryButtonClass}
          aria-label="Attach file"
        >
          <Paperclip size={18} />
        </button>

        <input
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              handleSubmit();
            }
          }}
          placeholder="Search for properties, ask about market trends, or compare areas..."
          className="
            min-w-0 flex-1 border-none bg-transparent px-1
            text-sm text-text-primary outline-none
            placeholder:text-text-muted
          "
        />

        <button
          type="button"
          className={`${secondaryButtonClass} hidden sm:flex`}
          aria-label="Search filters"
        >
          <SlidersHorizontal size={18} />
        </button>

        <button
          type="button"
          onClick={handleSubmit}
          disabled={!canSubmit}
          className="
            focus-ring flex size-10 shrink-0 items-center justify-center
            rounded-control bg-primary text-text-inverse
            transition-colors
            hover:bg-primary-hover
            active:bg-primary-active
            disabled:bg-surface-strong
            disabled:text-text-muted
          "
          aria-label="Send message"
        >
          <ArrowUp size={18} />
        </button>
      </div>

      <div className="mt-2 hidden items-center justify-center gap-4 border-t border-border pt-2 text-[11px] text-text-muted sm:flex">
        <button
          type="button"
          className="focus-ring flex items-center gap-1 rounded-control px-2 py-1 transition-colors hover:bg-primary-light hover:text-primary"
        >
          <MapPin size={12} />
          Use current location
        </button>

        <span>AI Market Insights</span>
      </div>
    </div>
  );
};
