import { Router, type IRouter } from "express";
import healthRouter from "./health";
import businessesRouter from "./businesses";
import alertsRouter from "./alerts";
import resolveRouter from "./resolve";
import statsRouter from "./stats";

const router: IRouter = Router();

router.use(healthRouter);
router.use(businessesRouter);
router.use(alertsRouter);
router.use(resolveRouter);
router.use(statsRouter);

export default router;
