import { Link, useLocation } from "wouter";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { Hexagon, Zap, Shield, Eye, Database } from "lucide-react";

export function AppSidebar() {
  const [location] = useLocation();

  const links = [
    { href: "/", label: "Overview", icon: Hexagon },
    { href: "/resolve", label: "Entity Resolution", icon: Database },
    { href: "/owner", label: "Owner Portal", icon: Shield },
    { href: "/officer", label: "Officer Dashboard", icon: Eye },
  ];

  return (
    <Sidebar className="border-r border-border bg-background">
      <SidebarHeader className="p-4">
        <Link href="/" className="flex items-center gap-2 px-2 py-1">
          <Zap className="h-6 w-6 text-primary" />
          <span className="font-heading font-bold text-xl tracking-wide text-foreground">
            BizPulse
          </span>
        </Link>
      </SidebarHeader>
      
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              {links.map((link) => {
                const isActive = location === link.href;
                return (
                  <SidebarMenuItem key={link.href}>
                    <SidebarMenuButton
                      asChild
                      isActive={isActive}
                      tooltip={link.label}
                      className="font-medium h-10"
                    >
                      <Link href={link.href} className="flex items-center gap-3">
                        <link.icon className={`h-4 w-4 ${isActive ? "text-primary" : "text-muted-foreground"}`} />
                        <span>{link.label}</span>
                      </Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="p-4 border-t border-border/50">
        <div className="flex flex-col gap-1 px-2">
          <span className="text-xs text-muted-foreground uppercase font-bold tracking-wider">
            Context
          </span>
          <span className="text-sm font-medium text-primary">
            {location.startsWith("/owner") ? "Business Owner" : 
             location.startsWith("/officer") ? "Government Officer" : 
             "Public Demo"}
          </span>
        </div>
      </SidebarFooter>
    </Sidebar>
  );
}
