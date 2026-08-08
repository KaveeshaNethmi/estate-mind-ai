import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ChatInput } from "../components/chat/ChatInput";
import { SuggestionCard } from "../components/chat/SuggestionCard";
import { WelcomeSection } from "../components/chat/WelcomeSection";
import { PageShell } from "../components/layout/PageShell";
import { TopNavigation } from "../components/layout/TopNavigation";
import { MarketPulsePanel } from "../components/market/MarketPulsePanel";
import { homeSuggestions } from "../data/homeSuggestions";
import type { AssistantMode } from "../types/assistantMode";
import { MobileModeTabs } from "../components/layout/MobileModeTabs";

export const HomePage = () => {
  const navigate = useNavigate();

  const [activeMode, setActiveMode] =
    useState<AssistantMode>("market-insights");

  const suggestions = homeSuggestions[activeMode];

  const handleSearch = (message: string) => {
    const searchParams = new URLSearchParams({
      q: message,
      mode: activeMode,
    });

    navigate(`/search?${searchParams.toString()}`);
  };

  return (
    <PageShell
      header={
        <TopNavigation activeMode={activeMode} onModeChange={setActiveMode} />
      }
      mobileSubHeader={
        <MobileModeTabs activeMode={activeMode} onModeChange={setActiveMode} />
      }
      rightPanel={<MarketPulsePanel />}
    >
      <div className="flex min-h-full flex-col bg-background">
        <main className="mx-auto flex w-full max-w-5xl flex-1 flex-col justify-center px-4 py-10 sm:px-6 lg:px-10">
          <WelcomeSection activeMode={activeMode} />

          <section className="mx-auto mt-10 grid w-full max-w-3xl grid-cols-1 gap-3 sm:grid-cols-2">
            {suggestions.map((suggestion) => (
              <SuggestionCard
                key={suggestion.id}
                label={suggestion.label}
                title={suggestion.title}
                description={suggestion.description}
                icon={suggestion.icon}
                onClick={() => handleSearch(suggestion.prompt)}
              />
            ))}
          </section>
        </main>

        <div className="sticky bottom-0 bg-background/95 px-4 py-4 backdrop-blur sm:px-6 lg:px-10">
          <div className="mx-auto w-full max-w-3xl">
            <ChatInput onSubmit={handleSearch} />
          </div>
        </div>
      </div>
    </PageShell>
  );
};
