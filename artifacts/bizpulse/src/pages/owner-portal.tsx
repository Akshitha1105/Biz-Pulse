import { useGetBusiness } from "@workspace/api-client-react";
import { Bell, CheckCircle2, AlertTriangle, XCircle, FileText, CalendarDays, ExternalLink, Download } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";

export default function OwnerPortal() {
  const ubid = "KA-2024-BIZ-002";
  const { data: business, isLoading } = useGetBusiness(ubid, {
    query: { enabled: true, queryKey: ['/api/businesses', ubid] }
  });

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-white">Owner Portal</h1>
          <p className="text-muted-foreground mt-1">Welcome back, Meena Sharma.</p>
        </div>
        <div className="relative">
          <Button variant="outline" size="icon" className="rounded-full border-border bg-card relative">
            <Bell className="h-5 w-5" />
            <span className="absolute top-0 right-0 w-2.5 h-2.5 bg-destructive rounded-full border-2 border-background animate-pulse" />
          </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: UBID Card & Actions */}
        <div className="lg:col-span-1 space-y-6">
          {isLoading ? (
            <Skeleton className="h-64 w-full rounded-2xl" />
          ) : (
            <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-card via-[#112646] to-card border border-primary/30 shadow-lg shadow-primary/5">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary/0 via-primary to-primary/0" />
              <div className="p-6">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <div className="text-[10px] uppercase tracking-widest text-primary font-bold mb-1">Government of Karnataka</div>
                    <div className="text-xs text-muted-foreground">Unified Business Identity</div>
                  </div>
                  <Badge variant="outline" className="bg-primary/10 text-primary border-primary/20">
                    {business?.status}
                  </Badge>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <div className="text-xs text-muted-foreground uppercase tracking-wider mb-1">UBID Number</div>
                    <div className="text-2xl font-mono font-bold text-white tracking-widest drop-shadow-sm">
                      {business?.ubid}
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="text-xs text-muted-foreground uppercase tracking-wider mb-1">Entity Name</div>
                      <div className="font-semibold text-white truncate" title={business?.name}>{business?.name}</div>
                    </div>
                    <div>
                      <div className="text-xs text-muted-foreground uppercase tracking-wider mb-1">Sector</div>
                      <div className="font-semibold text-white truncate">{business?.sector}</div>
                    </div>
                  </div>
                  
                  <div className="pt-4 mt-2 border-t border-border/50 flex justify-between items-center text-xs text-muted-foreground">
                    <div>Issued: 12 Jan 2024</div>
                    <div className="flex gap-2">
                      <QrCodeMock />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          <Card className="bg-card border-border">
            <CardHeader className="pb-3">
              <CardTitle className="text-lg">Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button variant="outline" className="w-full justify-start text-left font-normal" data-testid="btn-download-ubid">
                <Download className="mr-2 h-4 w-4" /> Download UBID Certificate
              </Button>
              <Button variant="outline" className="w-full justify-start text-left font-normal border-destructive/30 text-destructive hover:bg-destructive/10 hover:text-destructive" data-testid="btn-pay-dues">
                <AlertTriangle className="mr-2 h-4 w-4" /> Pay Municipal Dues
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Right Column: Compliance & Docs */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="text-xl flex justify-between items-center">
                <span>Compliance Status</span>
                <span className="text-3xl font-bold text-primary">{business?.complianceScore || 0}<span className="text-lg text-muted-foreground">/100</span></span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <div className="space-y-4">
                  <Skeleton className="h-16 w-full" />
                  <Skeleton className="h-16 w-full" />
                </div>
              ) : (
                <div className="space-y-4">
                  {business?.compliance?.map((item: any, i: number) => {
                    let icon, colorClass, bgClass, borderClass;
                    if (item.status === 'compliant') {
                      icon = <CheckCircle2 className="h-5 w-5 text-primary" />;
                      colorClass = "text-primary";
                      bgClass = "bg-primary/5";
                      borderClass = "border-primary/20";
                    } else if (item.status === 'warning') {
                      icon = <AlertTriangle className="h-5 w-5 text-warning" />;
                      colorClass = "text-warning";
                      bgClass = "bg-warning/5";
                      borderClass = "border-warning/20";
                    } else {
                      icon = <XCircle className="h-5 w-5 text-destructive" />;
                      colorClass = "text-destructive";
                      bgClass = "bg-destructive/5";
                      borderClass = "border-destructive/20";
                    }

                    return (
                      <div key={i} className={`flex items-center justify-between p-4 rounded-lg border ${borderClass} ${bgClass}`}>
                        <div className="flex items-center gap-4">
                          <div className="bg-background rounded-full p-1 border border-border">
                            {icon}
                          </div>
                          <div>
                            <div className="font-semibold text-white">{item.department}</div>
                            <div className="text-sm text-muted-foreground">{item.note || `Status: ${item.status}`}</div>
                          </div>
                        </div>
                        {item.expiresAt && (
                          <div className="text-right">
                            <div className="text-xs text-muted-foreground uppercase tracking-wider mb-1">Expires</div>
                            <div className={`text-sm font-medium ${colorClass}`}>
                              {new Date(item.expiresAt).toLocaleDateString()}
                            </div>
                          </div>
                        )}
                        {!item.expiresAt && item.status === 'non_compliant' && (
                          <Button size="sm" variant="destructive" className="h-8">Fix Now</Button>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card className="bg-card border-border">
              <CardHeader className="pb-3">
                <CardTitle className="text-lg flex items-center gap-2">
                  <FileText className="h-5 w-5 text-primary" />
                  My Documents
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between items-center p-3 rounded bg-background border border-border">
                  <div className="text-sm font-medium text-white">GST Certificate</div>
                  <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground"><ExternalLink className="h-4 w-4" /></Button>
                </div>
                <div className="flex justify-between items-center p-3 rounded bg-background border border-border">
                  <div className="text-sm font-medium text-white">Udyam Registration</div>
                  <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground"><ExternalLink className="h-4 w-4" /></Button>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-card border-border">
              <CardHeader className="pb-3">
                <CardTitle className="text-lg flex items-center gap-2">
                  <CalendarDays className="h-5 w-5 text-primary" />
                  Upcoming Deadlines
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4 relative before:absolute before:inset-0 before:ml-2 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-border before:to-transparent">
                  <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                    <div className="flex items-center justify-center w-5 h-5 rounded-full border border-warning bg-card text-warning shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow z-10">
                      <div className="w-2 h-2 bg-warning rounded-full"></div>
                    </div>
                    <div className="w-[calc(100%-2rem)] md:w-[calc(50%-1.5rem)] p-3 rounded border border-warning/20 bg-warning/5 ml-4 md:ml-0">
                      <div className="text-xs text-warning font-bold mb-1">In 30 Days</div>
                      <div className="text-sm text-white font-medium">Municipal Licence Renewal</div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

function QrCodeMock() {
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="opacity-50">
      <path d="M3 3H10V10H3V3Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M14 3H21V10H14V3Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M3 14H10V21H3V14Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M14 14H17V17H14V14Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M18 18H21V21H18V18Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M14 18H18V21H14V18Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M18 14H21V18H18V14Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  )
}
