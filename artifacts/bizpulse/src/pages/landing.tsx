import { useState, useEffect } from "react";
import { Link } from "wouter";
import { useGetStats } from "@workspace/api-client-react";
import { ArrowRight, Database, Users, ShieldCheck, Activity } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

function AnimatedCounter({ end, duration = 2000, suffix = "" }: { end: number, duration?: number, suffix?: string }) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let startTime: number | null = null;
    let animationFrame: number;

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = timestamp - startTime;
      const percentage = Math.min(progress / duration, 1);
      
      // Easing function
      const easeOutQuart = 1 - Math.pow(1 - percentage, 4);
      setCount(Math.floor(end * easeOutQuart));

      if (percentage < 1) {
        animationFrame = requestAnimationFrame(animate);
      }
    };

    animationFrame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationFrame);
  }, [end, duration]);

  return <>{count.toLocaleString()}{suffix}</>;
}

export default function LandingPage() {
  const { data: stats, isLoading } = useGetStats();

  return (
    <div className="space-y-24 animate-in fade-in duration-700">
      {/* Hero Section */}
      <section className="space-y-8 max-w-4xl pt-12">
        <div className="inline-flex items-center rounded-full border border-primary/30 bg-primary/10 px-3 py-1 text-sm text-primary font-medium">
          <Activity className="mr-2 h-4 w-4" />
          Live Platform Status: Optimal
        </div>
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white leading-tight">
          One Identity for <br />
          Every Business in <span className="text-primary">Karnataka</span>
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl">
          BizPulse replaces bureaucratic fragmentation with unified intelligence. 
          A single digital identity across all government departments for faster compliance, 
          better oversight, and zero friction.
        </p>
        <div className="flex gap-4">
          <Button asChild size="lg" className="h-12 px-8 bg-primary hover:bg-primary/90 text-primary-foreground font-bold">
            <Link href="/owner" data-testid="btn-owner-login">
              Business Owner Login
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </Button>
          <Button asChild variant="outline" size="lg" className="h-12 px-8 border-primary/30 hover:bg-primary/10 text-white">
            <Link href="/officer" data-testid="btn-officer-login">
              Government Officer Login
            </Link>
          </Button>
        </div>
      </section>

      {/* Stats Grid */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="p-8 border-border bg-card/50 backdrop-blur-sm">
          <div className="space-y-2">
            <div className="flex items-center text-primary mb-4">
              <Database className="h-6 w-6 mr-2" />
              <h3 className="font-semibold text-lg">Businesses Unified</h3>
            </div>
            <div className="text-4xl font-bold text-white tracking-tight">
              {isLoading ? <Skeleton className="h-10 w-32" /> : <AnimatedCounter end={stats?.totalBusinesses || 473291} />}
            </div>
          </div>
        </Card>
        
        <Card className="p-8 border-border bg-card/50 backdrop-blur-sm">
          <div className="space-y-2">
            <div className="flex items-center text-primary mb-4">
              <Users className="h-6 w-6 mr-2" />
              <h3 className="font-semibold text-lg">Districts Active</h3>
            </div>
            <div className="text-4xl font-bold text-white tracking-tight">
              {isLoading ? <Skeleton className="h-10 w-16" /> : <AnimatedCounter end={stats?.districtsActive || 31} />}
            </div>
          </div>
        </Card>

        <Card className="p-8 border-border bg-card/50 backdrop-blur-sm">
          <div className="space-y-2">
            <div className="flex items-center text-primary mb-4">
              <ShieldCheck className="h-6 w-6 mr-2" />
              <h3 className="font-semibold text-lg">Compliance Rate</h3>
            </div>
            <div className="text-4xl font-bold text-white tracking-tight">
              {isLoading ? <Skeleton className="h-10 w-24" /> : <AnimatedCounter end={stats?.complianceRate || 94.2} suffix="%" />}
            </div>
          </div>
        </Card>
      </section>

      {/* Story Section */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
        <div className="space-y-6">
          <h2 className="text-3xl font-bold text-white">The Fragmented Past</h2>
          <p className="text-lg text-muted-foreground leading-relaxed">
            Meena runs a textile factory in Hubli. Last year, she had to visit the GST portal, 
            the Udyam registry, the municipal office, and FSSAI separately just to renew her licenses. 
            Her identity existed in 4 different formats, spelled 3 different ways.
          </p>
          <div className="space-y-4">
            {["GSTIN: 29ABCDE1234F1Z5", "Udyam: UDYAM-KA-24-0012345", "Municipal: HUB-TRD-2023-89"].map((id, i) => (
              <div key={i} className="flex items-center p-4 rounded-lg bg-card/30 border border-destructive/20 text-muted-foreground">
                <span className="w-2 h-2 rounded-full bg-destructive mr-4" />
                {id}
              </div>
            ))}
          </div>
        </div>

        <div className="relative h-[400px] rounded-2xl border border-primary/20 bg-card overflow-hidden flex flex-col items-center justify-center p-8 text-center space-y-6">
          <div className="absolute inset-0 bg-primary/5 pattern-dots pointer-events-none" />
          <h3 className="text-2xl font-bold text-white relative z-10">The Unified Future</h3>
          <div className="relative z-10 flex items-center justify-center w-full">
            <div className="p-6 rounded-2xl bg-gradient-to-br from-primary/20 to-primary/5 border border-primary text-center">
              <span className="text-sm font-bold text-primary uppercase tracking-widest mb-2 block">Unified Business ID</span>
              <span className="text-3xl font-mono text-white font-bold tracking-tight">KA-2024-BIZ-002</span>
            </div>
          </div>
          <p className="text-primary relative z-10 font-medium">One ID. All Departments.</p>
        </div>
      </section>
    </div>
  );
}
