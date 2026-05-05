import { ReactNode } from "react";
import { AppSidebar } from "./app-sidebar";
import { SidebarProvider } from "@/components/ui/sidebar";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="flex h-screen bg-background overflow-hidden text-foreground selection:bg-primary/30">
      <AppSidebar />
      <main className="flex-1 overflow-y-auto w-full relative">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-primary/10 via-background to-background pointer-events-none" />
        <div className="relative z-10 p-6 md:p-8 lg:p-12 w-full max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}
