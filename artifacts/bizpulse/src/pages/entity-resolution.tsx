import { useState } from "react";
import { useResolveEntities } from "@workspace/api-client-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Database, Search, CheckCircle2, ChevronRight, Fingerprint, MapPin, Hash } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { Progress } from "@/components/ui/progress";

const MOCK_RECORDS = [
  { source: "GST Portal", name: "Meena Textiles", pan: "ABCDE1234F", address: "Plot 42, Hubli Ind Area" },
  { source: "Udyam Registry", name: "Meena Textile Mfg", pan: "ABCDE1234F", address: "P-42, Hubballi Industrial" },
  { source: "Municipal Corp", name: "Meena Textiles Co", pan: null, address: "42, Industrial Area, Hubli" },
  { source: "FSSAI", name: "M Textiles Canteen", pan: "ABCDE1234F", address: "Plot 42, Hubli" },
];

export default function EntityResolution() {
  const [step, setStep] = useState(0);
  const [isResolving, setIsResolving] = useState(false);
  const resolveMutation = useResolveEntities();
  const { toast } = useToast();

  const handleResolve = async () => {
    setIsResolving(true);
    setStep(1); // Name matching
    
    setTimeout(() => setStep(2), 1500); // PAN check
    setTimeout(() => setStep(3), 3000); // Address verify
    setTimeout(() => setStep(4), 4500); // Complete
    
    try {
      await resolveMutation.mutateAsync({
        data: { records: MOCK_RECORDS }
      });
      setTimeout(() => {
        setIsResolving(false);
        setStep(5);
        toast({
          title: "Resolution Complete",
          description: "Successfully unified 4 fragmented records into 1 UBID.",
        });
      }, 5500);
    } catch (e) {
      setIsResolving(false);
      setStep(0);
      toast({
        variant: "destructive",
        title: "Resolution Failed",
        description: "An error occurred during AI processing.",
      });
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">AI Entity Resolution</h1>
          <p className="text-muted-foreground mt-1">Deduplicating fragmented records into a Unified Business ID.</p>
        </div>
        <Button 
          size="lg" 
          onClick={handleResolve} 
          disabled={isResolving || step === 5}
          className="bg-primary text-primary-foreground hover:bg-primary/90 font-semibold"
          data-testid="btn-resolve"
        >
          {isResolving ? (
            <span className="flex items-center gap-2">
              <Search className="h-4 w-4 animate-spin" />
              Processing AI Match...
            </span>
          ) : step === 5 ? (
            <span className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4" />
              Resolution Complete
            </span>
          ) : (
            <span className="flex items-center gap-2">
              <Database className="h-4 w-4" />
              Run Entity Resolution
            </span>
          )}
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left: Input Records */}
        <div className="space-y-4 relative">
          <h2 className="text-xl font-semibold text-white flex items-center gap-2">
            Fragmented Databases <span className="bg-muted text-muted-foreground text-xs px-2 py-0.5 rounded-full">4 Records</span>
          </h2>
          
          <div className="space-y-3 relative z-10">
            {MOCK_RECORDS.map((record, i) => (
              <Card key={i} className={`p-4 bg-card/80 border-border ${step > 0 && 'opacity-50 transition-opacity duration-1000'}`}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-mono text-primary bg-primary/10 px-2 py-1 rounded">
                    {record.source}
                  </span>
                </div>
                <div className="font-semibold text-white">{record.name}</div>
                <div className="text-sm text-muted-foreground mt-2 grid grid-cols-2 gap-2">
                  <div className="flex items-center gap-1"><Hash className="h-3 w-3" /> {record.pan || 'Missing'}</div>
                  <div className="flex items-center gap-1 truncate" title={record.address}><MapPin className="h-3 w-3" /> {record.address}</div>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Right: Processing & Output */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-white">Unified Identity Engine</h2>
          
          <Card className="p-6 bg-card border-border h-[calc(100%-2.5rem)] flex flex-col justify-center">
            {step === 0 && (
              <div className="text-center space-y-4 text-muted-foreground">
                <Database className="h-12 w-12 mx-auto opacity-20" />
                <p>Waiting for input records to process...</p>
              </div>
            )}
            
            {step > 0 && step < 5 && (
              <div className="space-y-8 w-full">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-white flex items-center gap-2">
                      <Fingerprint className={`h-4 w-4 ${step >= 1 ? 'text-primary' : 'text-muted-foreground'}`} />
                      Fuzzy Name Matching
                    </span>
                    <span className="text-primary font-mono">{step >= 1 ? '92%' : '0%'}</span>
                  </div>
                  <Progress value={step >= 1 ? 92 : 0} className="h-2" />
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-white flex items-center gap-2">
                      <Hash className={`h-4 w-4 ${step >= 2 ? 'text-primary' : 'text-muted-foreground'}`} />
                      PAN Cross-Reference
                    </span>
                    <span className="text-primary font-mono">{step >= 2 ? '100%' : '0%'}</span>
                  </div>
                  <Progress value={step >= 2 ? 100 : 0} className="h-2" />
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-white flex items-center gap-2">
                      <MapPin className={`h-4 w-4 ${step >= 3 ? 'text-primary' : 'text-muted-foreground'}`} />
                      Address Vector Similarity
                    </span>
                    <span className="text-primary font-mono">{step >= 3 ? '85%' : '0%'}</span>
                  </div>
                  <Progress value={step >= 3 ? 85 : 0} className="h-2" />
                </div>
                
                {step >= 4 && (
                  <div className="pt-4 border-t border-border flex items-center justify-between text-white font-semibold">
                    <span>Overall Confidence Score</span>
                    <span className="text-2xl text-primary">92.3%</span>
                  </div>
                )}
              </div>
            )}

            {step === 5 && (
              <div className="space-y-6 text-center animate-in zoom-in duration-500">
                <div className="w-20 h-20 bg-primary/20 rounded-full flex items-center justify-center mx-auto border border-primary/50">
                  <CheckCircle2 className="h-10 w-10 text-primary" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-white mb-2">Entity Resolved</h3>
                  <p className="text-muted-foreground mb-6">4 fragmented records merged into a single truth.</p>
                  
                  <div className="bg-gradient-to-br from-primary/20 to-card border border-primary/30 rounded-xl p-6 relative overflow-hidden text-left">
                    <div className="absolute top-0 right-0 bg-primary/20 text-primary text-xs font-bold px-3 py-1 rounded-bl-lg uppercase tracking-wider">
                      UBID Assigned
                    </div>
                    <div className="text-sm text-muted-foreground mb-1">Unified Business Identifier</div>
                    <div className="text-2xl font-mono font-bold text-white tracking-widest mb-4">KA-2024-BIZ-002</div>
                    
                    <div className="grid grid-cols-2 gap-4 text-sm mt-4 pt-4 border-t border-primary/10">
                      <div>
                        <span className="text-muted-foreground block text-xs mb-1">Canonical Name</span>
                        <span className="text-white font-medium">Meena Textiles</span>
                      </div>
                      <div>
                        <span className="text-muted-foreground block text-xs mb-1">Primary PAN</span>
                        <span className="text-white font-medium">ABCDE1234F</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                <Button variant="outline" className="w-full mt-4" onClick={() => setStep(0)}>
                  Run Another Demo
                </Button>
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
}
