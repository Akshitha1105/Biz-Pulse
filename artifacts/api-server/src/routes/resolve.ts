import { Router, type IRouter } from "express";
import { ResolveEntitiesBody } from "@workspace/api-zod";

const router: IRouter = Router();

router.post("/resolve", (req, res) => {
  const parsed = ResolveEntitiesBody.safeParse(req.body);

  if (!parsed.success) {
    res.status(400).json({ error: "Invalid request body" });
    return;
  }

  const { records } = parsed.data;
  const start = Date.now();

  // Simulate grouping: every 3 records → 1 entity (matches the demo data)
  const chunkSize = 3;
  const resolvedEntities = [];

  const ubidMap = [
    { ubid: "KA-2024-BIZ-001", canonical: "Ravi Enterprises Pvt Ltd" },
    { ubid: "KA-2024-BIZ-002", canonical: "Meena Textiles" },
    { ubid: "KA-2024-BIZ-003", canonical: "Hubli Foods Co" },
  ];

  for (let i = 0; i < records.length; i += chunkSize) {
    const chunk = records.slice(i, i + chunkSize);
    const entityIndex = Math.floor(i / chunkSize);
    const meta = ubidMap[entityIndex] ?? {
      ubid: `KA-2024-BIZ-${String(entityIndex + 1).padStart(3, "0")}`,
      canonical: chunk[0]?.name ?? "Unknown Entity",
    };

    // Mock confidence scores
    const fuzzyName = 85 + Math.floor(Math.random() * 14);
    const panCrossRef = chunk.some((r) => r.pan != null) ? 95 + Math.floor(Math.random() * 5) : 60 + Math.floor(Math.random() * 20);
    const addressSimilarity = 72 + Math.floor(Math.random() * 25);
    const overall = Math.round((fuzzyName * 0.4 + panCrossRef * 0.4 + addressSimilarity * 0.2));

    resolvedEntities.push({
      ubid: meta.ubid,
      canonicalName: meta.canonical,
      matchedRecords: chunk,
      scores: {
        fuzzyName,
        panCrossRef,
        addressSimilarity,
        overall,
      },
    });
  }

  const elapsed = Date.now() - start + 800; // Add realistic-looking processing time

  res.json({
    entities: resolvedEntities,
    totalInputRecords: records.length,
    totalResolved: resolvedEntities.length,
    processingTimeMs: elapsed,
  });
});

export default router;
