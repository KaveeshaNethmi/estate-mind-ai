import {
  Bookmark,
  Clock3,
  MessageSquarePlus,
  Settings,
  Sparkles,
} from "lucide-react";
import { NavLink } from "react-router-dom";

const navigationItems = [
  {
    label: "New Chat",
    path: "/",
    icon: MessageSquarePlus,
  },
  {
    label: "History",
    path: "/history",
    icon: Clock3,
  },
  {
    label: "Saved Properties",
    path: "/saved-properties",
    icon: Bookmark,
  },
  {
    label: "Settings",
    path: "/settings",
    icon: Settings,
  },
];

export const LeftSidebar = () => {
  return (
    <aside className="fixed inset-y-0 left-0 z-40 hidden border-r border-border bg-background md:flex md:w-[72px] md:flex-col xl:w-[232px]">
      <div className="flex h-16 items-center px-4">
        <div className="flex items-center gap-2">
          <div className="flex size-9 items-center justify-center rounded-xl bg-primary text-white">
            <Sparkles size={18} />
          </div>

          <div className="hidden xl:block">
            <p className="text-xl font-bold text-primary">
              EstateMind AI
            </p>
            <p className="text-[10px] text-text-secondary">
              Premium Advisor
            </p>
          </div>
        </div>
      </div>

      <nav className="flex flex-1 flex-col gap-1 px-3 py-5">
        {navigationItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                [
                  "flex min-h-10 items-center justify-center gap-3 rounded-lg px-3 text-sm font-medium transition-colors xl:justify-start",
                  isActive
                    ? "bg-primary text-text-inverse"
                    : "text-text-secondary hover:bg-primary-light hover:text-primary",
                ].join(" ")
              }
            >
              <Icon size={18} />

              <span className="hidden xl:inline">{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="p-3">
        <div className="flex items-center justify-center gap-3 xl:justify-start">
          <div className="flex size-9 shrink-0 items-center justify-center rounded-full bg-primary-light text-xs font-semibold">
            KN
          </div>

          <div className="hidden min-w-0 xl:block">
            <p className="truncate text-xs font-semibold text-text-primary">
              Kaveesha Nethmi
            </p>

            <p className="truncate text-[10px] text-text-inverse-secondary">
              Free Workspace
            </p>
          </div>
        </div>
      </div>
    </aside>
  );
}