import type { LucideIcon } from "lucide-react";
import { ArrowUpRight } from "lucide-react";

interface SuggestionCardProps {
  label: string;
  title: string;
  description: string;
  icon: LucideIcon;
  onClick?: () => void;
}

export const SuggestionCard = ({
  label,
  title,
  description,
  icon: Icon,
  onClick,
}: SuggestionCardProps) => {
  return (
    <button
      type="button"
      onClick={onClick}
      className="
        focus-ring group flex min-h-32 w-full flex-col
        rounded-card border border-border bg-surface p-4 text-left
        shadow-card transition-all
        hover:-translate-y-0.5
        hover:border-border-primary
        hover:shadow-card-hover
      "
    >
      <div className="mb-3 flex items-start justify-between gap-3">
        <div className="flex items-center gap-2 text-primary">
          <Icon size={16} />

          <span className="text-[11px] font-semibold uppercase tracking-wide">
            {label}
          </span>
        </div>

        <ArrowUpRight
          size={16}
          className="text-text-muted transition-colors group-hover:text-primary"
        />
      </div>

      <h3 className="text-sm font-semibold text-text-primary">{title}</h3>

      <p className="mt-1 text-xs leading-5 text-text-secondary">
        {description}
      </p>
    </button>
  );
};
