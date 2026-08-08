import { createBrowserRouter } from "react-router-dom";
import { DashboardLayout } from "../layouts/DashboardLayout";
import { HomePage } from "../pages/HomePage";
import { SearchResultsPage } from "../pages/SearchResultsPage";
import { PropertyDetailsPage } from "../pages/PropertyDetailsPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <DashboardLayout />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: "search",
        element: <SearchResultsPage />,
      },
      {
        path: "properties/:propertyId",
        element: <PropertyDetailsPage />,
      },
      {
        path: "history",
        element: <div className="p-6">History</div>,
      },
      {
        path: "saved-properties",
        element: <div className="p-6">Saved Properties</div>,
      },
      {
        path: "settings",
        element: <div className="p-6">Settings</div>,
      },
    ],
  },
]);