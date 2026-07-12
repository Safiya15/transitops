const express = require('express');
const router = express.Router();
const pool = require('../db');
const { requireAuth, requireRole } = require('../middleware/auth');

router.use(requireAuth);

// GET /api/fuel/logs
router.get('/logs', async (req, res) => {
  try {
    const [rows] = await pool.query(
      `SELECT f.*, v.reg_no, v.name AS vehicle_name
       FROM fuel_logs f JOIN vehicles v ON v.id = f.vehicle_id
       ORDER BY f.log_date DESC`
    );
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch fuel logs' });
  }
});

// POST /api/fuel/logs
router.post('/logs', requireRole('Fleet Manager', 'Financial Analyst', 'Driver'), async (req, res) => {
  try {
    const { vehicle_id, log_date, liters, cost } = req.body;
    if (!vehicle_id || !log_date || !liters || !cost) {
      return res.status(400).json({ error: 'vehicle_id, log_date, liters and cost are required' });
    }
    const [result] = await pool.query(
      'INSERT INTO fuel_logs (vehicle_id, log_date, liters, cost) VALUES (?, ?, ?, ?)',
      [vehicle_id, log_date, liters, cost]
    );
    const [rows] = await pool.query('SELECT * FROM fuel_logs WHERE id = ?', [result.insertId]);
    res.status(201).json(rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to log fuel entry' });
  }
});

// GET /api/fuel/expenses
router.get('/expenses', async (req, res) => {
  try {
    const [rows] = await pool.query(
      `SELECT e.*, v.reg_no, v.name AS vehicle_name
       FROM expenses e JOIN vehicles v ON v.id = e.vehicle_id
       ORDER BY e.expense_date DESC`
    );
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch expenses' });
  }
});

// POST /api/fuel/expenses
router.post('/expenses', requireRole('Fleet Manager', 'Financial Analyst', 'Driver'), async (req, res) => {
  try {
    const { vehicle_id, expense_type, cost, expense_date } = req.body;
    if (!vehicle_id || !expense_type || !cost || !expense_date) {
      return res.status(400).json({ error: 'vehicle_id, expense_type, cost and expense_date are required' });
    }
    const [result] = await pool.query(
      'INSERT INTO expenses (vehicle_id, expense_type, cost, expense_date) VALUES (?, ?, ?, ?)',
      [vehicle_id, expense_type, cost, expense_date]
    );
    const [rows] = await pool.query('SELECT * FROM expenses WHERE id = ?', [result.insertId]);
    res.status(201).json(rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to log expense' });
  }
});

// GET /api/fuel/operational-cost
// Total Operational Cost (Fuel + Maintenance + Other Expenses) per vehicle
router.get('/operational-cost', async (req, res) => {
  try {
    const [rows] = await pool.query(`
      SELECT
        v.id AS vehicle_id, v.reg_no, v.name,
        COALESCE(f.fuel_total, 0) AS fuel_total,
        COALESCE(m.maintenance_total, 0) AS maintenance_total,
        COALESCE(e.expense_total, 0) AS other_expense_total,
        (COALESCE(f.fuel_total, 0) + COALESCE(m.maintenance_total, 0) + COALESCE(e.expense_total, 0)) AS total_operational_cost
      FROM vehicles v
      LEFT JOIN (SELECT vehicle_id, SUM(cost) AS fuel_total FROM fuel_logs GROUP BY vehicle_id) f ON f.vehicle_id = v.id
      LEFT JOIN (SELECT vehicle_id, SUM(cost) AS maintenance_total FROM maintenance_logs GROUP BY vehicle_id) m ON m.vehicle_id = v.id
      LEFT JOIN (SELECT vehicle_id, SUM(cost) AS expense_total FROM expenses GROUP BY vehicle_id) e ON e.vehicle_id = v.id
      ORDER BY total_operational_cost DESC
    `);
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to compute operational cost' });
  }
});

module.exports = router;
