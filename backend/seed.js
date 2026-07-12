const bcrypt = require('bcryptjs');
const pool = require('./db');

async function seed() {
  console.log('Seeding TransitOps demo data...');

  // --- Users (one per role) ---
  const users = [
    { name: 'Raven K.', email: 'fleet@transitops.demo', role: 'Fleet Manager', password: 'password123' },
    { name: 'Alex Driver', email: 'driver@transitops.demo', role: 'Driver', password: 'password123' },
    { name: 'Priya Safety', email: 'safety@transitops.demo', role: 'Safety Officer', password: 'password123' },
    { name: 'Sam Finance', email: 'finance@transitops.demo', role: 'Financial Analyst', password: 'password123' }
  ];
  for (const u of users) {
    const hash = await bcrypt.hash(u.password, 10);
    await pool.query(
      'INSERT IGNORE INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)',
      [u.name, u.email, hash, u.role]
    );
  }

  // --- Vehicles (matches the mockup) ---
  const vehicles = [
    ['GJ01AB4521', 'VAN-05', 'Van', 500, 74000, 620000, 'Available', 'West'],
    ['GJ01AB9987', 'TRUCK-11', 'Truck', 5000, 182000, 2450000, 'Available', 'West'],
    ['GJ01AB1120', 'MINI-03', 'Mini', 1000, 66000, 410000, 'Available', 'North'],
    ['GJ01AB0081', 'VAN-09', 'Van', 750, 241900, 590000, 'Retired', 'North']
  ];
  for (const v of vehicles) {
    await pool.query(
      `INSERT IGNORE INTO vehicles (reg_no, name, type, max_load_capacity, odometer, acquisition_cost, status, region)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
      v
    );
  }

  // --- Drivers (matches the mockup) ---
  const drivers = [
    ['Alex', 'DL-88213', 'LMV', '2028-12-31', '9876500001', 96, 'Available'],
    ['John', 'DL-44120', 'HMV', '2025-03-31', '9822000002', 81, 'Suspended'],
    ['Priya', 'DL-77031', 'LMV', '2028-08-20', '9911000003', 99, 'On Trip'],
    ['Suresh', 'DL-90045', 'HMV', '2027-01-15', '9744000004', 88, 'Available']
  ];
  for (const d of drivers) {
    await pool.query(
      `INSERT IGNORE INTO drivers (name, license_number, license_category, license_expiry, contact_number, safety_score, status)
       VALUES (?, ?, ?, ?, ?, ?, ?)`,
      d
    );
  }

  console.log('Seed complete. Demo logins (password: password123):');
  users.forEach(u => console.log(`  ${u.role}: ${u.email}`));
  process.exit(0);
}

seed().catch(err => {
  console.error('Seed failed:', err);
  process.exit(1);
});
