import { Bell, Bookmark, Moon, Share2 } from "lucide-react";
import { assistantModes } from "../../data/assistantModes";
import type { AssistantMode } from "../../types/assistantMode";

interface TopNavigationProps {
  activeMode?: AssistantMode;
  onModeChange?: (mode: AssistantMode) => void;
  showModes?: boolean;
}

export const TopNavigation = ({
  activeMode = "market-insights",
  onModeChange,
  showModes = true,
}: TopNavigationProps) => {
  const iconButtonClass =
    "focus-ring flex size-9 items-center justify-center rounded-control text-text-muted transition-colors hover:bg-surface-subtle hover:text-text-primary";

  return (
    <header className="flex h-16 items-center justify-between bg-background px-4 sm:px-6">
      {/* LEFT SIDE */}
      <div className="flex min-w-0 items-center gap-5">
        {/* Mobile brand */}
        <div className="md:hidden">
          <p className="text-sm font-bold text-text-primary">
            EstateMind AI
          </p>

          <p className="text-[10px] font-medium uppercase tracking-wide text-primary">
            Premium AI Advisor
          </p>
        </div>

        {/* Desktop assistant modes */}
        {showModes && (
          <nav
            aria-label="Assistant modes"
            className="hidden h-16 min-w-0 items-center gap-5 md:flex"
          >
            {assistantModes.map((mode) => {
              const isActive = activeMode === mode.id;

              return (
                <button
                  key={mode.id}
                  type="button"
                  onClick={() => onModeChange?.(mode.id)}
                  className={[
                    "focus-ring relative flex h-full shrink-0 items-center px-1 text-sm font-medium transition-colors",
                    isActive
                      ? "text-primary"
                      : "text-text-secondary hover:text-text-primary",
                  ].join(" ")}
                >
                  {mode.label}

                  <span
                    aria-hidden="true"
                    className={[
                      "absolute inset-x-0 bottom-0 h-0.5 rounded-pill",
                      isActive ? "bg-primary" : "bg-transparent",
                    ].join(" ")}
                  />
                </button>
              );
            })}
          </nav>
        )}
      </div>

      {/* RIGHT SIDE */}
      <div className="flex shrink-0 items-center gap-1">
        <button
          type="button"
          className={`${iconButtonClass} hidden lg:flex`}
          aria-label="Saved properties"
        >
          <Bookmark size={18} />
        </button>

        <button
          type="button"
          className={`${iconButtonClass} hidden sm:flex`}
          aria-label="Change theme"
        >
          <Moon size={18} />
        </button>

        <button
          type="button"
          className={iconButtonClass}
          aria-label="Notifications"
        >
          <Bell size={18} />
        </button>

        <button
          type="button"
          className={`${iconButtonClass} hidden sm:flex`}
          aria-label="Share"
        >
          <Share2 size={18} />
        </button>
      </div>
    </header>
  );
};