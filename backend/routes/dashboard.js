const express = require('express');
const router = express.Router();
const pool = require('../db');
const { requireAuth } = require('../middleware/auth');

router.use(requireAuth);

// GET /api/dashboard/kpis?type=&region=
router.get('/kpis', async (req, res) => {
  try {
    const { type, region } = req.query;
    let vehicleFilter = 'WHERE 1=1';
    const params = [];
    if (type && type !== 'All') { vehicleFilter += ' AND type = ?'; params.push(type); }
    if (region && region !== 'All') { vehicleFilter += ' AND region = ?'; params.push(region); }

    const [[vehicleCounts]] = await pool.query(
      `SELECT
         COUNT(*) AS total_vehicles,
         SUM(status IN ('Available','On Trip')) AS active_vehicles,
         SUM(status = 'Available') AS available_vehicles,
         SUM(status = 'In Shop') AS in_shop_vehicles
       FROM vehicles ${vehicleFilter}`,
      params
    );

    const [[tripCounts]] = await pool.query(
      `SELECT
         SUM(status = 'Dispatched') AS active_trips,
         SUM(status = 'Draft') AS pending_trips
       FROM trips`
    );

    const [[driverCounts]] = await pool.query(
      `SELECT SUM(status = 'On Trip') AS drivers_on_duty FROM drivers`
    );

    const totalVehicles = vehicleCounts.total_vehicles || 0;
    const activeVehicles = vehicleCounts.active_vehicles || 0;
    const fleetUtilization = totalVehicles > 0
      ? Number(((activeVehicles / totalVehicles) * 100).toFixed(1))
      : 0;

    res.json({
      active_vehicles: activeVehicles,
      available_vehicles: vehicleCounts.available_vehicles || 0,
      in_shop_vehicles: vehicleCounts.in_shop_vehicles || 0,
      active_trips: tripCounts.active_trips || 0,
      pending_trips: tripCounts.pending_trips || 0,
      drivers_on_duty: driverCounts.drivers_on_duty || 0,
      fleet_utilization_pct: fleetUtilization
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to compute dashboard KPIs' });
  }
});

module.exports = router;
