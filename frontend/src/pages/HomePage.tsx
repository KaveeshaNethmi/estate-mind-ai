import { useState } from "react";

import { ChatInput } from "../components/chat/ChatInput";
import { SuggestionCard } from "../components/chat/SuggestionCard";
import { WelcomeSection } from "../components/chat/WelcomeSection";
import { MobileModeTabs } from "../components/layout/MobileModeTabs";
import { PageShell } from "../components/layout/PageShell";
import { TopNavigation } from "../components/layout/TopNavigation";
import { MarketPulsePanel } from "../components/market/MarketPulsePanel";

import { homeSuggestions } from "../data/homeSuggestions";
import { useChat } from "../hooks/useChat";

import type { AssistantMode } from "../types/assistantMode";
import { ChatConversation } from "../components/chat/chatConversation";

export function HomePage() {
  const [activeMode, setActiveMode] =
    useState<AssistantMode>("market-insights");

  const {
    messages,
    isStreaming,
    error,
    sendMessage,
  } = useChat();

  const suggestions = homeSuggestions[activeMode];

  const hasConversation = messages.length > 0;

  return (
    <PageShell
      header={
        <TopNavigation
          activeMode={activeMode}
          onModeChange={setActiveMode}
        />
      }
      mobileSubHeader={
        <MobileModeTabs
          activeMode={activeMode}
          onModeChange={setActiveMode}
        />
      }
      rightPanel={<MarketPulsePanel />}
    >
      <div className="flex min-h-full flex-col bg-background">
        {!hasConversation ? (
          <main
            className="
              mx-auto flex w-full max-w-5xl flex-1 flex-col
              px-4 py-7
              sm:px-6 sm:py-10
              lg:justify-center lg:px-10
            "
          >
            <WelcomeSection
              activeMode={activeMode}
            />

            <section
              className="
                mx-auto mt-7 grid w-full max-w-3xl
                grid-cols-1 gap-3
                sm:mt-10 sm:grid-cols-2
              "
            >
              {suggestions.map((suggestion) => (
                <SuggestionCard
                  key={suggestion.id}
                  label={suggestion.label}
                  title={suggestion.title}
                  description={
                    suggestion.description
                  }
                  icon={suggestion.icon}
                  onClick={() =>
                    sendMessage(suggestion.prompt)
                  }
                />
              ))}
            </section>
          </main>
        ) : (
          <main className="min-h-0 flex-1">
            <ChatConversation
              messages={messages}
            />
          </main>
        )}

        {error && (
          <div className="mx-auto w-full max-w-3xl px-4">
            <div
              className="
                rounded-control bg-error-light
                px-3 py-2 text-sm text-error
              "
            >
              {error}
            </div>
          </div>
        )}

        <div
          className="
            sticky bottom-16 z-20
            bg-background/95 px-3 py-3
            backdrop-blur
            md:bottom-0
            sm:px-6
            lg:px-10
          "
        >
          <div className="mx-auto w-full max-w-3xl">
            <ChatInput
              onSubmit={sendMessage}
              disabled={isStreaming}
            />
          </div>
        </div>
      </div>
    </PageShell>
  );
}