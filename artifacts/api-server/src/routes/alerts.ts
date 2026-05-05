import { Router, type IRouter } from "express";
import { intelligenceAlerts } from "./mockData";

const router: IRouter = Router();

router.get("/alerts", (_req, res) => {
  res.json(intelligenceAlerts);
});

export default router;
