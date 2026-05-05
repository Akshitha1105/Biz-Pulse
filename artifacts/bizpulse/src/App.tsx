import { Switch, Route, Router as WouterRouter } from "wouter";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { SidebarProvider } from "@/components/ui/sidebar";

import Layout from "@/components/layout";
import LandingPage from "@/pages/landing";
import EntityResolution from "@/pages/entity-resolution";
import OwnerPortal from "@/pages/owner-portal";
import OfficerDashboard from "@/pages/officer-dashboard";
import BusinessProfile from "@/pages/business-profile";
import NotFound from "@/pages/not-found";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function Router() {
  return (
    <Layout>
      <Switch>
        <Route path="/" component={LandingPage} />
        <Route path="/resolve" component={EntityResolution} />
        <Route path="/owner" component={OwnerPortal} />
        <Route path="/officer" component={OfficerDashboard} />
        <Route path="/business/:ubid" component={BusinessProfile} />
        <Route component={NotFound} />
      </Switch>
    </Layout>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <SidebarProvider>
          <WouterRouter base={import.meta.env.BASE_URL.replace(/\/$/, "")}>
            <Router />
          </WouterRouter>
        </SidebarProvider>
        <Toaster />
      </TooltipProvider>
    </QueryClientProvider>
  );
}

export default App;
