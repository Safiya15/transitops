const express = require('express');
const router = express.Router();
const pool = require('../db');
const { requireAuth, requireRole } = require('../middleware/auth');

router.use(requireAuth);

// Generates a simple sequential trip code like TR001, TR002...
async function nextTripCode() {
  const [rows] = await pool.query('SELECT COUNT(*) AS cnt FROM trips');
  const n = rows[0].cnt + 1;
  return `TR${String(n).padStart(3, '0')}`;
}

// Shared validation used both on create and on dispatch, so the rule can
// never be bypassed regardless of which endpoint is hit.
async function validateAssignment({ vehicleId, driverId, cargoWeight, excludeTripId = null }) {
  const [[vehicle]] = await pool.query('SELECT * FROM vehicles WHERE id = ?', [vehicleId]);
  const [[driver]] = await pool.query('SELECT * FROM drivers WHERE id = ?', [driverId]);

  if (!vehicle) return { ok: false, error: 'Vehicle not found' };
  if (!driver) return { ok: false, error: 'Driver not found' };

  // Retired or In Shop vehicles must never appear in dispatch
  if (['Retired', 'In Shop'].includes(vehicle.status)) {
    return { ok: false, error: `Vehicle ${vehicle.reg_no} is ${vehicle.status} and cannot be dispatched` };
  }
  // Vehicle already On Trip cannot be assigned to another trip
  if (vehicle.status === 'On Trip') {
    return { ok: false, error: `Vehicle ${vehicle.reg_no} is already On Trip` };
  }

  // Expired license or Suspended -> blocked from trip assignment
  const today = new Date().toISOString().slice(0, 10);
  if (driver.license_expiry < today) {
    return { ok: false, error: `Driver ${driver.name}'s license expired on ${driver.license_expiry}` };
  }
  if (driver.status === 'Suspended') {
    return { ok: false, error: `Driver ${driver.name} is Suspended` };
  }
  if (driver.status === 'On Trip') {
    return { ok: false, error: `Driver ${driver.name} is already On Trip` };
  }

  // Cargo weight must not exceed vehicle's max load capacity
  if (Number(cargoWeight) > Number(vehicle.max_load_capacity)) {
    const over = Number(cargoWeight) - Number(vehicle.max_load_capacity);
    return {
      ok: false,
      error: `Vehicle Capacity: ${vehicle.max_load_capacity} kg, Cargo Weight: ${cargoWeight} kg — Capacity exceeded by ${over} kg, dispatch blocked`
    };
  }

  return { ok: true, vehicle, driver };
}

// GET /api/trips?status=
router.get('/', async (req, res) => {
  try {
    const { status } = req.query;
    let sql = `
      SELECT t.*, v.reg_no, v.name AS vehicle_name, d.name AS driver_name
      FROM trips t
      JOIN vehicles v ON v.id = t.vehicle_id
      JOIN drivers d ON d.id = t.driver_id
      WHERE 1=1`;
    const params = [];
    if (status && status !== 'All') { sql += ' AND t.status = ?'; params.push(status); }
    sql += ' ORDER BY t.created_at DESC';
    const [rows] = await pool.query(sql, params);
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch trips' });
  }
});

// POST /api/trips - create a Draft trip
router.post('/', requireRole('Fleet Manager', 'Driver'), async (req, res) => {
  try {
    const { source, destination, vehicle_id, driver_id, cargo_weight, planned_distance } = req.body;
    if (!source || !destination || !vehicle_id || !driver_id || !cargo_weight || !planned_distance) {
      return res.status(400).json({ error: 'source, destination, vehicle_id, driver_id, cargo_weight and planned_distance are required' });
    }

    const check = await validateAssignment({ vehicleId: vehicle_id, driverId: driver_id, cargoWeight: cargo_weight });
    if (!check.ok) return res.status(422).json({ error: check.error });

    const trip_code = await nextTripCode();
    const [result] = await pool.query(
      `INSERT INTO trips (trip_code, source, destination, vehicle_id, driver_id, cargo_weight, planned_distance, status)
       VALUES (?, ?, ?, ?, ?, ?, ?, 'Draft')`,
      [trip_code, source, destination, vehicle_id, driver_id, cargo_weight, planned_distance]
    );
    const [rows] = await pool.query('SELECT * FROM trips WHERE id = ?', [result.insertId]);
    res.status(201).json(rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to create trip' });
  }
});

// POST /api/trips/:id/dispatch
// Re-validates (in case status changed since the trip was drafted), then
// flips both vehicle and driver to "On Trip".
router.post('/:id/dispatch', requireRole('Fleet Manager', 'Driver'), async (req, res) => {
  const conn = await pool.getConnection();
  try {
    const { id } = req.params;
    const [[trip]] = await conn.query('SELECT * FROM trips WHERE id = ?', [id]);
    if (!trip) return res.status(404).json({ error: 'Trip not found' });
    if (trip.status !== 'Draft') return res.status(409).json({ error: `Only Draft trips can be dispatched (current status: ${trip.status})` });

    const check = await validateAssignment({ vehicleId: trip.vehicle_id, driverId: trip.driver_id, cargoWeight: trip.cargo_weight });
    if (!check.ok) return res.status(422).json({ error: check.error });

    await conn.beginTransaction();
    await conn.query("UPDATE trips SET status = 'Dispatched', dispatched_at = NOW() WHERE id = ?", [id]);
    await conn.query("UPDATE vehicles SET status = 'On Trip' WHERE id = ?", [trip.vehicle_id]);
    await conn.query("UPDATE drivers SET status = 'On Trip' WHERE id = ?", [trip.driver_id]);
    await conn.commit();

    const [rows] = await pool.query('SELECT * FROM trips WHERE id = ?', [id]);
    res.json(rows[0]);
  } catch (err) {
    await conn.rollback();
    console.error(err);
    res.status(500).json({ error: 'Failed to dispatch trip' });
  } finally {
    conn.release();
  }
});

// POST /api/trips/:id/complete
// Body: { final_odometer, fuel_consumed, fuel_cost }
// Flow: odometer -> fuel log -> expenses -> Vehicle & Driver Available
router.post('/:id/complete', requireRole('Fleet Manager', 'Driver'), async (req, res) => {
  const conn = await pool.getConnection();
  try {
    const { id } = req.params;
    const { final_odometer, fuel_consumed, fuel_cost } = req.body;
    if (final_odometer === undefined || fuel_consumed === undefined) {
      return res.status(400).json({ error: 'final_odometer and fuel_consumed are required' });
    }

    const [[trip]] = await conn.query('SELECT * FROM trips WHERE id = ?', [id]);
    if (!trip) return res.status(404).json({ error: 'Trip not found' });
    if (trip.status !== 'Dispatched') return res.status(409).json({ error: `Only Dispatched trips can be completed (current status: ${trip.status})` });

    await conn.beginTransaction();

    await conn.query(
      "UPDATE trips SET status = 'Completed', completed_at = NOW(), final_odometer = ?, fuel_consumed = ? WHERE id = ?",
      [final_odometer, fuel_consumed, id]
    );
    await conn.query('UPDATE vehicles SET odometer = ?, status = \'Available\' WHERE id = ?', [final_odometer, trip.vehicle_id]);
    await conn.query("UPDATE drivers SET status = 'Available' WHERE id = ?", [trip.driver_id]);

    if (fuel_cost !== undefined) {
      await conn.query(
        'INSERT INTO fuel_logs (vehicle_id, log_date, liters, cost) VALUES (?, CURDATE(), ?, ?)',
        [trip.vehicle_id, fuel_consumed, fuel_cost]
      );
    }

    await conn.commit();
    const [rows] = await pool.query('SELECT * FROM trips WHERE id = ?', [id]);
    res.json(rows[0]);
  } catch (err) {
    await conn.rollback();
    console.error(err);
    res.status(500).json({ error: 'Failed to complete trip' });
  } finally {
    conn.release();
  }
});

// POST /api/trips/:id/cancel
// Cancelling a Dispatched trip restores vehicle and driver to Available.
// Cancelling a Draft trip just marks it Cancelled (nothing to restore).
router.post('/:id/cancel', requireRole('Fleet Manager', 'Driver'), async (req, res) => {
  const conn = await pool.getConnection();
  try {
    const { id } = req.params;
    const [[trip]] = await conn.query('SELECT * FROM trips WHERE id = ?', [id]);
    if (!trip) return res.status(404).json({ error: 'Trip not found' });
    if (!['Draft', 'Dispatched'].includes(trip.status)) {
      return res.status(409).json({ error: `Cannot cancel a trip that is already ${trip.status}` });
    }

    await conn.beginTransaction();
    await conn.query("UPDATE trips SET status = 'Cancelled' WHERE id = ?", [id]);
    if (trip.status === 'Dispatched') {
      await conn.query("UPDATE vehicles SET status = 'Available' WHERE id = ?", [trip.vehicle_id]);
      await conn.query("UPDATE drivers SET status = 'Available' WHERE id = ?", [trip.driver_id]);
    }
    await conn.commit();

    const [rows] = await pool.query('SELECT * FROM trips WHERE id = ?', [id]);
    res.json(rows[0]);
  } catch (err) {
    await conn.rollback();
    console.error(err);
    res.status(500).json({ error: 'Failed to cancel trip' });
  } finally {
    conn.release();
  }
});

module.exports = router;
