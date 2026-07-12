const express = require('express');
const router = express.Router();
const pool = require('../db');
const { requireAuth } = require('../middleware/auth');

router.use(requireAuth);

// NOTE on Revenue for ROI: the PS defines
//   Vehicle ROI = (Revenue - (Maintenance + Fuel)) / Acquisition Cost
// but does not specify where "Revenue" comes from. Since TransitOps has no
// billing/invoicing module, we estimate revenue from completed trips using
// a configurable rate-per-km. Adjust REVENUE_RATE_PER_KM to match whatever
// your hackathon judges expect, or wire this to a real revenue field later.
const REVENUE_RATE_PER_KM = 25; // currency units per km, placeholder assumption

// GET /api/reports/summary
router.get('/summary', async (req, res) => {
  try {
    // Fuel Efficiency = total distance / total fuel (across completed trips)
    const [[fuelEff]] = await pool.query(`
      SELECT
        COALESCE(SUM(planned_distance), 0) AS total_distance,
        COALESCE(SUM(fuel_consumed), 0) AS total_fuel
      FROM trips WHERE status = 'Completed'
    `);
    const fuelEfficiency = fuelEff.total_fuel > 0
      ? Number((fuelEff.total_distance / fuelEff.total_fuel).toFixed(2))
      : 0;

    // Fleet Utilization = active vehicles / total vehicles
    const [[fleet]] = await pool.query(`
      SELECT COUNT(*) AS total, SUM(status IN ('Available','On Trip')) AS active FROM vehicles
    `);
    const fleetUtilization = fleet.total > 0
      ? Number(((fleet.active / fleet.total) * 100).toFixed(1))
      : 0;

    // Operational Cost = Fuel + Maintenance (+ other expenses)
    const [[cost]] = await pool.query(`
      SELECT
        (SELECT COALESCE(SUM(cost),0) FROM fuel_logs) +
        (SELECT COALESCE(SUM(cost),0) FROM maintenance_logs) +
        (SELECT COALESCE(SUM(cost),0) FROM expenses) AS total_operational_cost
    `);

    // Monthly revenue (last 6 months) from completed trips, for the bar chart
    const [monthlyRevenue] = await pool.query(`
      SELECT DATE_FORMAT(completed_at, '%b') AS month,
             SUM(planned_distance) * ? AS revenue
      FROM trips
      WHERE status = 'Completed' AND completed_at >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
      GROUP BY DATE_FORMAT(completed_at, '%Y-%m'), month
      ORDER BY MIN(completed_at)
    `, [REVENUE_RATE_PER_KM]);

    res.json({
      fuel_efficiency_km_per_l: fuelEfficiency,
      fleet_utilization_pct: fleetUtilization,
      operational_cost: cost.total_operational_cost || 0,
      revenue_rate_per_km_assumption: REVENUE_RATE_PER_KM,
      monthly_revenue: monthlyRevenue
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to compute report summary' });
  }
});

// GET /api/reports/vehicle-roi - ROI per vehicle
router.get('/vehicle-roi', async (req, res) => {
  try {
    const [rows] = await pool.query(`
      SELECT
        v.id, v.reg_no, v.name, v.acquisition_cost,
        COALESCE(f.fuel_total, 0) AS fuel_total,
        COALESCE(m.maintenance_total, 0) AS maintenance_total,
        COALESCE(t.distance_total, 0) * ? AS estimated_revenue
      FROM vehicles v
      LEFT JOIN (SELECT vehicle_id, SUM(cost) AS fuel_total FROM fuel_logs GROUP BY vehicle_id) f ON f.vehicle_id = v.id
      LEFT JOIN (SELECT vehicle_id, SUM(cost) AS maintenance_total FROM maintenance_logs GROUP BY vehicle_id) m ON m.vehicle_id = v.id
      LEFT JOIN (SELECT vehicle_id, SUM(planned_distance) AS distance_total FROM trips WHERE status = 'Completed' GROUP BY vehicle_id) t ON t.vehicle_id = v.id
    `, [REVENUE_RATE_PER_KM]);

    const withRoi = rows.map(r => {
      const costs = Number(r.fuel_total) + Number(r.maintenance_total);
      const roi = r.acquisition_cost > 0
        ? Number((((r.estimated_revenue - costs) / r.acquisition_cost) * 100).toFixed(2))
        : 0;
      return { ...r, roi_pct: roi };
    });

    res.json(withRoi);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to compute vehicle ROI' });
  }
});

// GET /api/reports/export.csv - CSV export of the operational cost report
router.get('/export.csv', async (req, res) => {
  try {
    const [rows] = await pool.query(`
      SELECT
        v.reg_no, v.name, v.type, v.status,
        COALESCE(f.fuel_total, 0) AS fuel_cost,
        COALESCE(m.maintenance_total, 0) AS maintenance_cost,
        (COALESCE(f.fuel_total, 0) + COALESCE(m.maintenance_total, 0)) AS total_operational_cost
      FROM vehicles v
      LEFT JOIN (SELECT vehicle_id, SUM(cost) AS fuel_total FROM fuel_logs GROUP BY vehicle_id) f ON f.vehicle_id = v.id
      LEFT JOIN (SELECT vehicle_id, SUM(cost) AS maintenance_total FROM maintenance_logs GROUP BY vehicle_id) m ON m.vehicle_id = v.id
    `);

    const header = 'Reg No,Name,Type,Status,Fuel Cost,Maintenance Cost,Total Operational Cost\n';
    const csvBody = rows.map(r =>
      [r.reg_no, r.name, r.type, r.status, r.fuel_cost, r.maintenance_cost, r.total_operational_cost].join(',')
    ).join('\n');

    res.setHeader('Content-Type', 'text/csv');
    res.setHeader('Content-Disposition', 'attachment; filename="transitops-report.csv"');
    res.send(header + csvBody);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to export CSV' });
  }
});

module.exports = router;
