const express = require('express');
const router = express.Router();
const pool = require('../db');
const { requireAuth, requireRole } = require('../middleware/auth');

router.use(requireAuth);

// GET /api/vehicles?type=&status=&region=&search=
router.get('/', async (req, res) => {
  try {
    const { type, status, region, search } = req.query;
    let sql = 'SELECT * FROM vehicles WHERE 1=1';
    const params = [];

    if (type && type !== 'All') { sql += ' AND type = ?'; params.push(type); }
    if (status && status !== 'All') { sql += ' AND status = ?'; params.push(status); }
    if (region && region !== 'All') { sql += ' AND region = ?'; params.push(region); }
    if (search) { sql += ' AND reg_no LIKE ?'; params.push(`%${search}%`); }

    sql += ' ORDER BY created_at DESC';
    const [rows] = await pool.query(sql, params);
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch vehicles' });
  }
});

// GET /api/vehicles/available - only vehicles eligible for dispatch
router.get('/available', async (req, res) => {
  try {
    const [rows] = await pool.query("SELECT * FROM vehicles WHERE status = 'Available'");
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch available vehicles' });
  }
});

// POST /api/vehicles - Fleet Manager only
router.post('/', requireRole('Fleet Manager'), async (req, res) => {
  try {
    const { reg_no, name, type, max_load_capacity, odometer, acquisition_cost, region } = req.body;
    if (!reg_no || !name || !type || !max_load_capacity) {
      return res.status(400).json({ error: 'reg_no, name, type and max_load_capacity are required' });
    }

    // Enforce: registration number must be unique
    const [existing] = await pool.query('SELECT id FROM vehicles WHERE reg_no = ?', [reg_no]);
    if (existing.length > 0) {
      return res.status(409).json({ error: `Registration number '${reg_no}' is already in use` });
    }

    const [result] = await pool.query(
      `INSERT INTO vehicles (reg_no, name, type, max_load_capacity, odometer, acquisition_cost, region, status)
       VALUES (?, ?, ?, ?, ?, ?, ?, 'Available')`,
      [reg_no, name, type, max_load_capacity, odometer || 0, acquisition_cost || 0, region || null]
    );
    const [rows] = await pool.query('SELECT * FROM vehicles WHERE id = ?', [result.insertId]);
    res.status(201).json(rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to create vehicle' });
  }
});

// PUT /api/vehicles/:id - Fleet Manager only
router.put('/:id', requireRole('Fleet Manager'), async (req, res) => {
  try {
    const { id } = req.params;
    const { name, type, max_load_capacity, odometer, acquisition_cost, region, status } = req.body;

    const [existing] = await pool.query('SELECT * FROM vehicles WHERE id = ?', [id]);
    if (existing.length === 0) return res.status(404).json({ error: 'Vehicle not found' });

    await pool.query(
      `UPDATE vehicles SET name=?, type=?, max_load_capacity=?, odometer=?, acquisition_cost=?, region=?, status=?
       WHERE id = ?`,
      [
        name ?? existing[0].name,
        type ?? existing[0].type,
        max_load_capacity ?? existing[0].max_load_capacity,
        odometer ?? existing[0].odometer,
        acquisition_cost ?? existing[0].acquisition_cost,
        region ?? existing[0].region,
        status ?? existing[0].status,
        id
      ]
    );
    const [rows] = await pool.query('SELECT * FROM vehicles WHERE id = ?', [id]);
    res.json(rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to update vehicle' });
  }
});

// DELETE /api/vehicles/:id - Fleet Manager only
router.delete('/:id', requireRole('Fleet Manager'), async (req, res) => {
  try {
    await pool.query('DELETE FROM vehicles WHERE id = ?', [req.params.id]);
    res.json({ success: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to delete vehicle (it may have linked trips/logs)' });
  }
});

module.exports = router;
