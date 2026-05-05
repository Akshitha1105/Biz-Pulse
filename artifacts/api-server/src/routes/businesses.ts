import { Router, type IRouter } from "express";
import { businesses } from "./mockData";

const router: IRouter = Router();

router.get("/businesses", (req, res) => {
  const { sector, city, status, search } = req.query as {
    sector?: string;
    city?: string;
    status?: string;
    search?: string;
  };

  let results = [...businesses];

  if (sector) {
    results = results.filter((b) => b.sector.toLowerCase() === sector.toLowerCase());
  }
  if (city) {
    results = results.filter((b) => b.city.toLowerCase() === city.toLowerCase());
  }
  if (status) {
    results = results.filter((b) => b.status.toLowerCase() === status.toLowerCase());
  }
  if (search) {
    const q = search.toLowerCase();
    results = results.filter(
      (b) =>
        b.name.toLowerCase().includes(q) ||
        b.ubid.toLowerCase().includes(q) ||
        b.owner.toLowerCase().includes(q) ||
        b.city.toLowerCase().includes(q)
    );
  }

  res.json(results);
});

router.get("/businesses/:ubid", (req, res) => {
  const { ubid } = req.params;
  const business = businesses.find((b) => b.ubid === ubid);

  if (!business) {
    res.status(404).json({ error: `Business with UBID ${ubid} not found` });
    return;
  }

  res.json(business);
});

export default router;
