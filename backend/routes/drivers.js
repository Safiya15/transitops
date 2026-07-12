const express = require('express');
const router = express.Router();
const pool = require('../db');
const { requireAuth, requireRole } = require('../middleware/auth');

router.use(requireAuth);

// GET /api/drivers?status=&search=
router.get('/', async (req, res) => {
  try {
    const { status, search } = req.query;
    let sql = 'SELECT * FROM drivers WHERE 1=1';
    const params = [];
    if (status && status !== 'All') { sql += ' AND status = ?'; params.push(status); }
    if (search) { sql += ' AND name LIKE ?'; params.push(`%${search}%`); }
    sql += ' ORDER BY created_at DESC';
    const [rows] = await pool.query(sql, params);
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch drivers' });
  }
});

// GET /api/drivers/available - only drivers eligible for dispatch
// Rule: expired license OR Suspended status -> excluded
router.get('/available', async (req, res) => {
  try {
    const [rows] = await pool.query(
      `SELECT * FROM drivers
       WHERE status = 'Available' AND license_expiry >= CURDATE()`
    );
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch available drivers' });
  }
});

// POST /api/drivers - Fleet Manager or Safety Officer
router.post('/', requireRole('Fleet Manager', 'Safety Officer'), async (req, res) => {
  try {
    const { name, license_number, license_category, license_expiry, contact_number, safety_score } = req.body;
    if (!name || !license_number || !license_category || !license_expiry || !contact_number) {
      return res.status(400).json({ error: 'name, license_number, license_category, license_expiry and contact_number are required' });
    }

    const [existing] = await pool.query('SELECT id FROM drivers WHERE license_number = ?', [license_number]);
    if (existing.length > 0) {
      return res.status(409).json({ error: `License number '${license_number}' is already registered` });
    }

    const [result] = await pool.query(
      `INSERT INTO drivers (name, license_number, license_category, license_expiry, contact_number, safety_score, status)
       VALUES (?, ?, ?, ?, ?, ?, 'Available')`,
      [name, license_number, license_category, license_expiry, contact_number, safety_score ?? 100]
    );
    const [rows] = await pool.query('SELECT * FROM drivers WHERE id = ?', [result.insertId]);
    res.status(201).json(rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to create driver' });
  }
});

// PUT /api/drivers/:id - Fleet Manager or Safety Officer
// Safety Officer typically toggles status (e.g. Suspended); Fleet Manager can edit all fields
router.put('/:id', requireRole('Fleet Manager', 'Safety Officer'), async (req, res) => {
  try {
    const { id } = req.params;
    const { name, license_category, license_expiry, contact_number, safety_score, status } = req.body;

    const [existing] = await pool.query('SELECT * FROM drivers WHERE id = ?', [id]);
    if (existing.length === 0) return res.status(404).json({ error: 'Driver not found' });

    // A driver currently On Trip cannot be silently reassigned to another status by mistake
    if (existing[0].status === 'On Trip' && status && status !== 'On Trip') {
      return res.status(409).json({ error: 'Cannot change status of a driver who is currently On Trip. Complete or cancel their trip first.' });
    }

    await pool.query(
      `UPDATE drivers SET name=?, license_category=?, license_expiry=?, contact_number=?, safety_score=?, status=?
       WHERE id = ?`,
      [
        name ?? existing[0].name,
        license_category ?? existing[0].license_category,
        license_expiry ?? existing[0].license_expiry,
        contact_number ?? existing[0].contact_number,
        safety_score ?? existing[0].safety_score,
        status ?? existing[0].status,
        id
      ]
    );
    const [rows] = await pool.query('SELECT * FROM drivers WHERE id = ?', [id]);
    res.json(rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to update driver' });
  }
});

// DELETE /api/drivers/:id - Fleet Manager only
router.delete('/:id', requireRole('Fleet Manager'), async (req, res) => {
  try {
    await pool.query('DELETE FROM drivers WHERE id = ?', [req.params.id]);
    res.json({ success: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to delete driver (they may have linked trips)' });
  }
});

module.exports = router;
