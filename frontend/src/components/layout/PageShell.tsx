import type { ReactNode } from "react";

interface PageShellProps {
  children: ReactNode;
  header?: ReactNode;
  mobileSubHeader?: ReactNode;
  rightPanel?: ReactNode;
}

export const PageShell = ({
  children,
  header,
  mobileSubHeader,
  rightPanel,
}: PageShellProps) => {
  return (
    <div className="flex h-screen min-w-0 flex-col overflow-hidden bg-background">
      {header && <div className="shrink-0 bg-background">{header}</div>}
      {mobileSubHeader && (
        <div className="shrink-0 bg-background md:hidden">
          {mobileSubHeader}
        </div>
      )}
      <div className="flex min-h-0 flex-1 overflow-hidden">
        <section className="min-w-0 flex-1 overflow-y-auto bg-background">
          {children}
        </section>

        {rightPanel && (
          <aside className="hidden h-full w-[320px] shrink-0 overflow-y-auto border-l border-border bg-background xl:block">
            {rightPanel}
          </aside>
        )}
      </div>
    </div>
  );
};
