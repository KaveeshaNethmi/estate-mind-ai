import { Building2, ChartNoAxesCombined } from "lucide-react";
import type { AssistantMode } from "../../types/assistantMode";

interface WelcomeSectionProps {
  activeMode: AssistantMode;
}

const welcomeContent: Record<
  AssistantMode,
  {
    eyebrow: string;
    title: string;
    description: string;
  }
> = {
  "market-insights": {
    eyebrow: "EstateMind AI",
    title: "How can I help you find your home in Dubai today?",
    description:
      "Ask me about neighbourhoods, investment yields, off-plan properties, or homes that match your lifestyle.",
  },

  "investment-analysis": {
    eyebrow: "AI Investment Analysis",
    title: "Let’s evaluate your next Dubai property investment",
    description:
      "Compare properties, analyse rental returns, understand market demand, and identify opportunities that match your budget.",
  },
};

export const WelcomeSection = ({ activeMode }: WelcomeSectionProps) => {
  const content = welcomeContent[activeMode];
  const Icon =
    activeMode === "market-insights" ? Building2 : ChartNoAxesCombined;

  return (
    <section className="mx-auto w-full max-w-3xl text-center">
      <div
        className="
    mx-auto mb-4 flex size-10 items-center justify-center
    rounded-card bg-primary-light text-primary shadow-card
    sm:mb-5 sm:size-12
  "
      >
        <Icon size={24} />
      </div>

      <p className="mb-2 text-sm font-semibold text-primary">
        {content.eyebrow}
      </p>

      <h1
        className="
    text-2xl font-bold tracking-tight text-text-primary
    sm:text-3xl
    lg:text-[2.75rem] lg:leading-[1.08]
  "
      >
        {content.title}
      </h1>

      <p
        className="
    mx-auto mt-3 max-w-2xl
    text-sm leading-6 text-text-secondary
    sm:mt-4 sm:text-base
  "
      >
        {content.description}
      </p>
    </section>
  );
};
