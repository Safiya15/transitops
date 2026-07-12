# TransitOps — Smart Transport Operations Platform

A working starter build covering every module in the problem statement:
Auth+RBAC, Dashboard, Vehicle Registry, Driver Management, Trip Dispatcher,
Maintenance, Fuel & Expenses, Reports & Analytics (CSV export).

Stack: **Node.js + Express + MySQL** backend, **vanilla HTML/CSS/JS** frontend
(no build tools — open the files directly, or serve with any static server).

---

## 1. Backend setup (do this first, ~10 min)

```bash
cd backend
npm install
cp .env.example .env
```

Edit `.env` with your local MySQL credentials.

Create the database and tables:

```bash
mysql -u root -p < schema.sql
```

Seed demo data (4 users, 4 vehicles, 4 drivers matching the mockup):

```bash
npm run seed
```

Start the API:

```bash
npm start
```

Runs on `http://localhost:5000`. Health check: `GET /api/health`.

### Demo logins (password for all: `password123`)
| Role | Email |
|---|---|
| Fleet Manager | fleet@transitops.demo |
| Driver | driver@transitops.demo |
| Safety Officer | safety@transitops.demo |
| Financial Analyst | finance@transitops.demo |

---

## 2. Frontend setup

No build step. Easiest options:

```bash
cd frontend
npx serve .
# or: python3 -m http.server 8080
```

Then open `login.html` (or `index.html`) in the browser. It talks to the
API at `http://localhost:5000/api` — change `API_BASE` in `js/app.js` if
your backend runs elsewhere.

---

## 3. What's already wired up

- **JWT auth + RBAC** — `middleware/auth.js` enforces roles per-route
  (e.g. only Fleet Manager can add vehicles). `settings.html` shows the
  matrix; the backend is the real source of truth.
- **Vehicle Registry** — unique reg_no enforced server-side, status enum
  (Available/On Trip/In Shop/Retired).
- **Driver Management** — expired-license and Suspended drivers are
  excluded from `/api/drivers/available` (used by the trip dispatcher).
- **Trip Dispatcher** — full lifecycle Draft → Dispatched → Completed →
  Cancelled, with the cargo-vs-capacity check, "already On Trip" checks,
  and automatic status flips on dispatch/complete/cancel (see
  `routes/trips.js`, function `validateAssignment`).
- **Maintenance** — creating a record flips the vehicle to In Shop;
  closing it restores Available (unless Retired).
- **Fuel & Expenses** — per-vehicle totals via `/api/fuel/operational-cost`.
- **Reports** — Fuel Efficiency, Fleet Utilization, Operational Cost,
  Vehicle ROI, CSV export. **Note:** the PS's ROI formula needs a
  "Revenue" figure that isn't defined anywhere else in the spec — this
  build estimates it from completed-trip distance × a placeholder rate
  (`REVENUE_RATE_PER_KM` in `routes/reports.js`). Change this if your
  judges expect something else, or ask them what they intend "Revenue"
  to mean.

## 4. What's NOT built (bonus features — add only if time remains)
- PDF export (CSV is done, PDF is optional per the PS)
- Email reminders for expiring licenses
- Vehicle document management
- Dark mode (the whole UI is already dark-themed by default, so this
  is arguably free — could add a light theme toggle instead if you want
  to literally tick the box)

## 5. Suggested team split for remaining hours
- Backend logic is done — spend time on: testing the exact example
  workflow from the PS end-to-end, seeding more realistic demo data,
  and polishing whichever bonus features you have time for.
- Whoever is strongest at UI: take frontend-design pass on charts /
  empty states / mobile responsiveness.
- Test the full flow: register Van-05 → register Alex → create 450kg
  trip → dispatch → complete → create maintenance record → check
  reports update.
