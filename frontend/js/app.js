// ============================================================
// Shared helpers used by every page. No build step, no framework —
// just fetch + localStorage, kept deliberately simple for an
// 8-hour build.
// ============================================================

const API_BASE = 'http://localhost:5000/api';

// ---------- Auth ----------
function getToken() { return localStorage.getItem('to_token'); }
function getUser() {
  const raw = localStorage.getItem('to_user');
  return raw ? JSON.parse(raw) : null;
}
function setSession(token, user) {
  localStorage.setItem('to_token', token);
  localStorage.setItem('to_user', JSON.stringify(user));
}
function logout() {
  localStorage.removeItem('to_token');
  localStorage.removeItem('to_user');
  window.location.href = 'login.html';
}
function requireLogin() {
  if (!getToken()) window.location.href = 'login.html';
}

// ---------- API client ----------
async function apiFetch(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  let data = null;
  try { data = await res.json(); } catch (e) { /* e.g. CSV export has no JSON body */ }

  if (!res.ok) {
    const message = (data && data.error) || `Request failed (${res.status})`;
    throw new Error(message);
  }
  return data;
}

// ---------- Sidebar ----------
const NAV_ITEMS = [
  { key: 'dashboard', label: 'Dashboard', href: 'dashboard.html' },
  { key: 'fleet', label: 'Fleet', href: 'vehicles.html' },
  { key: 'drivers', label: 'Drivers', href: 'drivers.html' },
  { key: 'trips', label: 'Trips', href: 'trips.html' },
  { key: 'maintenance', label: 'Maintenance', href: 'maintenance.html' },
  { key: 'fuel', label: 'Fuel & Expenses', href: 'fuel.html' },
  { key: 'analytics', label: 'Analytics', href: 'reports.html' },
  { key: 'settings', label: 'Settings', href: 'settings.html', roles: ['Fleet Manager'] }
];

function renderSidebar(activeKey) {
  const user = getUser();
  if (!user) return;
  const container = document.getElementById('sidebar');
  if (!container) return;

  const links = NAV_ITEMS
    .filter(item => !item.roles || item.roles.includes(user.role))
    .map(item => `<a class="nav-link ${item.key === activeKey ? 'active' : ''}" href="${item.href}">${item.label}</a>`)
    .join('');

  container.innerHTML = `
    <div class="brand"><span class="dot"></span> TransitOps</div>
    ${links}
    <div class="nav-spacer"></div>
    <div class="user-chip">
      <div class="name">${user.name}</div>
      <div class="role">${user.role}</div>
      <div class="logout" onclick="logout()">Log out</div>
    </div>
  `;
}

// ---------- Status pill ----------
const STATUS_COLOR = {
  'Available': 'green', 'Completed': 'green', 'Active': 'orange',
  'On Trip': 'blue', 'Dispatched': 'blue',
  'In Shop': 'orange', 'Draft': 'orange', 'Off Duty': 'orange',
  'Retired': 'red', 'Suspended': 'red', 'Cancelled': 'red'
};

function pill(status) {
  const color = STATUS_COLOR[status] || 'orange';
  return `<span class="pill pill-${color}"><span class="pulse"></span>${status}</span>`;
}

// ---------- Small utils ----------
function fmtMoney(n) {
  const num = Number(n || 0);
  return num.toLocaleString('en-IN', { maximumFractionDigits: 0 });
}
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str ?? '';
  return div.innerHTML;
}
function showAlert(containerId, message, type = 'error') {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = `<div class="alert alert-${type}">${escapeHtml(message)}</div>`;
}
function clearAlert(containerId) {
  const el = document.getElementById(containerId);
  if (el) el.innerHTML = '';
}
