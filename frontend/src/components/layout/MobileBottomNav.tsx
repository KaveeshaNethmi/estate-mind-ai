import {
  Bookmark,
  Home,
  MessageSquare,
  UserRound,
} from "lucide-react";
import { NavLink } from "react-router-dom";

const mobileNavigation = [
  {
    label: "Search",
    path: "/",
    icon: Home,
  },
  {
    label: "Chat",
    path: "/",
    icon: MessageSquare,
  },
  {
    label: "Saved",
    path: "/saved-properties",
    icon: Bookmark,
  },
  {
    label: "Profile",
    path: "/settings",
    icon: UserRound,
  },
];

export function MobileBottomNav() {
  return (
    <nav
      className="
        fixed inset-x-0 bottom-0 z-50
        flex h-16 items-center justify-around
        border-t border-border/60
        bg-background/95 px-2 backdrop-blur
        md:hidden
      "
    >
      {mobileNavigation.map((item) => {
        const Icon = item.icon;

        return (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              [
                "focus-ring flex min-w-14 flex-col items-center justify-center gap-1 rounded-control px-2 py-1 text-[10px] font-medium transition-colors",
                isActive
                  ? "text-primary"
                  : "text-text-muted hover:text-text-primary",
              ].join(" ")
            }
          >
            <Icon size={19} />

            <span>{item.label}</span>
          </NavLink>
        );
      })}
    </nav>
  );
}