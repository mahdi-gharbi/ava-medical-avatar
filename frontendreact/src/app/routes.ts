import { createBrowserRouter } from "react-router";
import { Layout } from "./components/Layout";
import { Dashboard } from "./pages/Dashboard";
import { TrainingMode } from "./pages/TrainingMode";
import { CommercialMode } from "./pages/CommercialMode";
import { MarketingIntelligence } from "./pages/MarketingIntelligence";
import { VisitIntelligence } from "./pages/VisitIntelligence";
import { BO5 } from "./pages/BO5";
import { Analytics } from "./pages/Analytics";
import { CRMIntegration } from "./pages/CRMIntegration";
import { Reports } from "./pages/Reports";
import { KnowledgeBase } from "./pages/KnowledgeBase";
import { Settings } from "./pages/Settings";
import { AdminPanel } from "./pages/AdminPanel";
import { SimulationConfig } from "./pages/SimulationConfig";
import { LiveSimulation } from "./pages/LiveSimulation";
import { PerformanceReport } from "./pages/PerformanceReport";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Layout,
    children: [
      { index: true, Component: Dashboard },
      { path: "training", Component: TrainingMode },
      { path: "commercial", Component: CommercialMode },
      { path: "marketing", Component: MarketingIntelligence },
      { path: "visit-intelligence", Component: VisitIntelligence },
      { path: "bo5", Component: BO5 },
      { path: "analytics", Component: Analytics },
      { path: "crm", Component: CRMIntegration },
      { path: "reports", Component: Reports },
      { path: "knowledge-base", Component: KnowledgeBase },
      { path: "settings", Component: Settings },
      { path: "admin", Component: AdminPanel },
      { path: "simulation-config", Component: SimulationConfig },
      { path: "performance-report", Component: PerformanceReport },
    ],
  },
  {
    path: "/live-simulation",
    Component: LiveSimulation,
  },
]);