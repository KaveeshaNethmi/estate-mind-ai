import { PageShell } from "../components/layout/PageShell";
import { TopNavigation } from "../components/layout/TopNavigation";

export const SearchResultsPage = () => {
  return (
    <PageShell
      header={
        <TopNavigation
          activeMode="market-insights"
          onModeChange={() => undefined}
        />
      }
      rightPanel={
        <aside className="h-full bg-background p-5">
          <h2 className="text-sm font-semibold text-text-primary">
            Search Properties
          </h2>

          <p className="mt-2 text-sm text-text-secondary">
            Property filters and matching results will appear here.
          </p>
        </aside>
      }
    >
      <div className="min-h-full bg-background p-6">
        <h1 className="text-2xl font-bold text-text-primary">
          Dubai Hills Project
        </h1>

        <p className="mt-2 text-sm text-text-secondary">
          The interactive map and search results will be implemented next.
        </p>
      </div>
    </PageShell>
  );
}