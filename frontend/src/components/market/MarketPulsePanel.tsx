import {
  ArrowUpRight,
  Building2,
  ChevronRight,
  TrendingUp,
} from "lucide-react";

const marketAreas = [
  {
    name: "Palm Jumeirah",
    type: "Luxury villas",
    growth: "+8.4%",
  },
  {
    name: "Dubai Marina",
    type: "Waterfront apartments",
    growth: "+6.8%",
  },
  {
    name: "Downtown Dubai",
    type: "Prime apartments",
    growth: "+5.9%",
  },
];

export const MarketPulsePanel = () => {
  return (
    <div className="flex h-full flex-col bg-background">
      <div className="p-5">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-primary">
              Live Market
            </p>

            <h2 className="mt-1 text-base font-semibold text-text-primary">
              Dubai Market Pulse
            </h2>
          </div>

          <div className="flex size-10 items-center justify-center rounded-card bg-primary-light text-primary">
            <TrendingUp size={19} />
          </div>
        </div>
      </div>

      <div className="flex-1 space-y-6 p-5">
        <section className="rounded-card  bg-surface-subtle p-4">
          <p className="text-xs font-medium text-text-secondary">
            Average price
          </p>

          <div className="mt-2 flex items-end justify-between gap-3">
            <div>
              <p className="text-2xl font-bold text-text-primary">1,245</p>

              <p className="text-xs text-text-muted">AED/sqft</p>
            </div>

            <span className="rounded-pill bg-success-light px-2.5 py-1 text-xs font-semibold text-success">
              +4.1%
            </span>
          </div>

          <div className="mt-5 flex h-16 items-end gap-1.5">
            {[28, 38, 34, 48, 55, 68, 77].map((height, index) => (
              <div
                key={`${height}-${index}`}
                className="flex-1 rounded-t-sm bg-secondary"
                style={{ height: `${height}%` }}
              />
            ))}
          </div>
        </section>

        <section>
          <div className="mb-3 flex items-center justify-between">
            <h3 className="text-xs font-semibold uppercase tracking-wide text-text-secondary">
              Hot areas right now
            </h3>

            <button
              type="button"
              className="focus-ring rounded-control px-2 py-1 text-xs font-semibold text-primary hover:bg-primary-light"
            >
              View all
            </button>
          </div>

          <div className="space-y-2">
            {marketAreas.map((area) => (
              <button
                key={area.name}
                type="button"
                className="
                  focus-ring flex w-full items-center gap-3 rounded-card
                  border border-transparent p-2 text-left
                  transition-colors
                  hover:border-border hover:bg-surface-subtle
                "
              >
                <div className="flex size-10 shrink-0 items-center justify-center rounded-control bg-tertiary-light text-tertiary">
                  <Building2 size={17} />
                </div>

                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-semibold text-text-primary">
                    {area.name}
                  </p>

                  <p className="truncate text-xs text-text-muted">
                    {area.type}
                  </p>
                </div>

                <div className="flex items-center gap-1">
                  <span className="text-xs font-semibold text-success">
                    {area.growth}
                  </span>

                  <ChevronRight size={15} className="text-text-muted" />
                </div>
              </button>
            ))}
          </div>
        </section>

        <section className="rounded-card border border-primary/15 bg-primary-light p-4">
          <div className="flex items-start gap-3">
            <div className="flex size-9 shrink-0 items-center justify-center rounded-control bg-surface text-primary shadow-card">
              <ArrowUpRight size={17} />
            </div>

            <div>
              <h3 className="text-sm font-semibold text-text-primary">
                Investment tip
              </h3>

              <p className="mt-1 text-xs leading-5 text-text-secondary">
                Rental demand remains strong in waterfront communities and
                established family neighbourhoods.
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};
