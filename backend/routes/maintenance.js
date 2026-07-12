const express = require('express');
const router = express.Router();
const pool = require('../db');
const { requireAuth, requireRole } = require('../middleware/auth');

router.use(requireAuth);

// GET /api/maintenance
router.get('/', async (req, res) => {
  try {
    const [rows] = await pool.query(
      `SELECT m.*, v.reg_no, v.name AS vehicle_name
       FROM maintenance_logs m
       JOIN vehicles v ON v.id = m.vehicle_id
       ORDER BY m.created_at DESC`
    );
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch maintenance logs' });
  }
});

// POST /api/maintenance
// Creating an Active maintenance record automatically switches vehicle to "In Shop"
router.post('/', requireRole('Fleet Manager'), async (req, res) => {
  const conn = await pool.getConnection();
  try {
    const { vehicle_id, service_type, cost, service_date } = req.body;
    if (!vehicle_id || !service_type || !service_date) {
      return res.status(400).json({ error: 'vehicle_id, service_type and service_date are required' });
    }

    const [[vehicle]] = await conn.query('SELECT * FROM vehicles WHERE id = ?', [vehicle_id]);
    if (!vehicle) return res.status(404).json({ error: 'Vehicle not found' });
    if (vehicle.status === 'On Trip') {
      return res.status(409).json({ error: 'Cannot log maintenance for a vehicle that is currently On Trip' });
    }

    await conn.beginTransaction();
    const [result] = await conn.query(
      `INSERT INTO maintenance_logs (vehicle_id, service_type, cost, service_date, status)
       VALUES (?, ?, ?, ?, 'Active')`,
      [vehicle_id, service_type, cost || 0, service_date]
    );
    // Adding to Maintenance Log automatically switches vehicle status to "In Shop"
    await conn.query("UPDATE vehicles SET status = 'In Shop' WHERE id = ?", [vehicle_id]);
    await conn.commit();

    const [rows] = await pool.query('SELECT * FROM maintenance_logs WHERE id = ?', [result.insertId]);
    res.status(201).json(rows[0]);
  } catch (err) {
    await conn.rollback();
    console.error(err);
    res.status(500).json({ error: 'Failed to create maintenance record' });
  } finally {
    conn.release();
  }
});

// POST /api/maintenance/:id/close
// Closing maintenance restores vehicle to Available (unless Retired)
router.post('/:id/close', requireRole('Fleet Manager'), async (req, res) => {
  const conn = await pool.getConnection();
  try {
    const { id } = req.params;
    const [[log]] = await conn.query('SELECT * FROM maintenance_logs WHERE id = ?', [id]);
    if (!log) return res.status(404).json({ error: 'Maintenance record not found' });
    if (log.status === 'Completed') return res.status(409).json({ error: 'This maintenance record is already closed' });

    const [[vehicle]] = await conn.query('SELECT * FROM vehicles WHERE id = ?', [log.vehicle_id]);

    await conn.beginTransaction();
    await conn.query("UPDATE maintenance_logs SET status = 'Completed' WHERE id = ?", [id]);
    if (vehicle.status !== 'Retired') {
      await conn.query("UPDATE vehicles SET status = 'Available' WHERE id = ?", [log.vehicle_id]);
    }
    await conn.commit();

    const [rows] = await pool.query('SELECT * FROM maintenance_logs WHERE id = ?', [id]);
    res.json(rows[0]);
  } catch (err) {
    await conn.rollback();
    console.error(err);
    res.status(500).json({ error: 'Failed to close maintenance record' });
  } finally {
    conn.release();
  }
});

module.exports = router;
