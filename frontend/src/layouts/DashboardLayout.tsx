import { Outlet } from "react-router-dom";
import { LeftSidebar } from "../components/layout/LeftSidebar";

export const DashboardLayout = () => {
  return (
    <div className="h-screen overflow-hidden bg-background text-text-primary">
      <LeftSidebar />

      <main className="h-screen overflow-hidden md:pl-[72px] xl:pl-[232px]">
        <Outlet />
      </main>
    </div>
  );
};
