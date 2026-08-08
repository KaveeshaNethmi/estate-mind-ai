import { assistantModes } from "../../data/assistantModes";
import type { AssistantMode } from "../../types/assistantMode";

interface MobileModeTabsProps {
  activeMode: AssistantMode;
  onModeChange: (mode: AssistantMode) => void;
}

export const MobileModeTabs = ({
  activeMode,
  onModeChange,
}: MobileModeTabsProps) => {
  return (
    <nav
      aria-label="Assistant modes"
      className="flex items-center gap-5 overflow-x-auto bg-background px-4 md:hidden"
    >
      {assistantModes.map((mode) => {
        const isActive = activeMode === mode.id;

        return (
          <button
            key={mode.id}
            type="button"
            onClick={() => onModeChange(mode.id)}
            className={[
              "focus-ring relative shrink-0 pb-2 pt-1 text-xs font-medium transition-colors",
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
  );
};
