import { Router, type IRouter } from "express";
import { platformStats, sectorAnalytics } from "./mockData";

const router: IRouter = Router();

router.get("/stats", (_req, res) => {
  res.json(platformStats);
});

router.get("/sector-analytics", (_req, res) => {
  res.json(sectorAnalytics);
});

export default router;
