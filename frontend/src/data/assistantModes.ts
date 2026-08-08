import type { AssistantMode } from "../types/assistantMode";

export interface AssistantModeOption {
  id: AssistantMode;
  label: string;
}

export const assistantModes: AssistantModeOption[] = [
  {
    id: "market-insights",
    label: "Market Insights",
  },
  {
    id: "investment-analysis",
    label: "Investment Analysis",
  },
];
