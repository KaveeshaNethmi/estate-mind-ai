import {
  Building2,
  ChartNoAxesCombined,
  Landmark,
  MapPin,
  Percent,
  Scale,
  TrendingUp,
  WalletCards,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import type { AssistantMode } from "../types/assistantMode";

export interface HomeSuggestion {
  id: string;
  label: string;
  title: string;
  description: string;
  prompt: string;
  icon: LucideIcon;
}

export const homeSuggestions: Record<
  AssistantMode,
  HomeSuggestion[]
> = {
  "market-insights": [
    {
      id: "palm-jumeirah-villas",
      label: "Luxury",
      title: "Luxury villas in Palm Jumeirah",
      description:
        "Explore premium waterfront homes with private amenities.",
      prompt:
        "Show me luxury villas available in Palm Jumeirah and explain the current market conditions.",
      icon: Building2,
    },
    {
      id: "best-investment-areas",
      label: "Market",
      title: "Best areas for investment",
      description:
        "Compare rental yields, buyer demand, and long-term growth.",
      prompt:
        "Which areas in Dubai currently offer the best property investment opportunities?",
      icon: TrendingUp,
    },
    {
      id: "downtown-apartments",
      label: "Location",
      title: "Apartments near Downtown Dubai",
      description:
        "Find homes close to business, dining, and entertainment.",
      prompt:
        "Find apartments near Downtown Dubai and compare their average prices.",
      icon: MapPin,
    },
    {
      id: "dubai-buying-guide",
      label: "Guide",
      title: "Dubai property buying guide",
      description:
        "Understand fees, ownership rules, and the buying process.",
      prompt:
        "Guide me through the process and costs of buying a property in Dubai.",
      icon: Landmark,
    },
  ],

  "investment-analysis": [
    {
      id: "high-rental-yield",
      label: "Rental Yield",
      title: "Properties with strong rental returns",
      description:
        "Discover areas and properties with attractive rental yields.",
      prompt:
        "Find Dubai properties with strong rental yields and explain the risks.",
      icon: Percent,
    },
    {
      id: "compare-investments",
      label: "Compare",
      title: "Compare two investment properties",
      description:
        "Evaluate price, yield, market demand, and appreciation potential.",
      prompt:
        "Help me compare two Dubai properties as investment opportunities.",
      icon: Scale,
    },
    {
      id: "investment-budget",
      label: "Budget",
      title: "Invest with a specific budget",
      description:
        "Find suitable properties based on your available capital.",
      prompt:
        "I have an investment budget of AED 2 million. What properties should I consider?",
      icon: WalletCards,
    },
    {
      id: "market-growth",
      label: "Forecast",
      title: "Areas with growth potential",
      description:
        "Explore communities with strong transaction and demand trends.",
      prompt:
        "Which Dubai areas have the strongest potential for property price growth?",
      icon: ChartNoAxesCombined,
    },
  ],
};