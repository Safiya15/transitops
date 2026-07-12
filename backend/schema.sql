-- TransitOps database schema
-- Run this once against a fresh MySQL database:
--   mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS transitops;
USE transitops;

-- ---------------------------------------------------------------
-- Users & Roles (Authentication + RBAC)
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(160) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('Fleet Manager', 'Driver', 'Safety Officer', 'Financial Analyst') NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------
-- Vehicles
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS vehicles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  reg_no VARCHAR(30) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  type VARCHAR(50) NOT NULL,
  max_load_capacity DECIMAL(10,2) NOT NULL,
  odometer DECIMAL(10,2) DEFAULT 0,
  acquisition_cost DECIMAL(12,2) DEFAULT 0,
  status ENUM('Available', 'On Trip', 'In Shop', 'Retired') NOT NULL DEFAULT 'Available',
  region VARCHAR(80) DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------
-- Drivers
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS drivers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  license_number VARCHAR(50) NOT NULL UNIQUE,
  license_category VARCHAR(20) NOT NULL,
  license_expiry DATE NOT NULL,
  contact_number VARCHAR(20) NOT NULL,
  safety_score INT DEFAULT 100,
  status ENUM('Available', 'On Trip', 'Off Duty', 'Suspended') NOT NULL DEFAULT 'Available',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------
-- Trips
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS trips (
  id INT AUTO_INCREMENT PRIMARY KEY,
  trip_code VARCHAR(20) NOT NULL UNIQUE,
  source VARCHAR(120) NOT NULL,
  destination VARCHAR(120) NOT NULL,
  vehicle_id INT NOT NULL,
  driver_id INT NOT NULL,
  cargo_weight DECIMAL(10,2) NOT NULL,
  planned_distance DECIMAL(10,2) NOT NULL,
  final_odometer DECIMAL(10,2) DEFAULT NULL,
  fuel_consumed DECIMAL(10,2) DEFAULT NULL,
  status ENUM('Draft', 'Dispatched', 'Completed', 'Cancelled') NOT NULL DEFAULT 'Draft',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  dispatched_at TIMESTAMP NULL,
  completed_at TIMESTAMP NULL,
  FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
  FOREIGN KEY (driver_id) REFERENCES drivers(id)
);

-- ---------------------------------------------------------------
-- Maintenance Logs
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS maintenance_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  vehicle_id INT NOT NULL,
  service_type VARCHAR(100) NOT NULL,
  cost DECIMAL(10,2) NOT NULL DEFAULT 0,
  service_date DATE NOT NULL,
  status ENUM('Active', 'Completed') NOT NULL DEFAULT 'Active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);

-- ---------------------------------------------------------------
-- Fuel Logs
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fuel_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  vehicle_id INT NOT NULL,
  log_date DATE NOT NULL,
  liters DECIMAL(10,2) NOT NULL,
  cost DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);

-- ---------------------------------------------------------------
-- Other Expenses (tolls, misc, maintenance mirrors also land here optionally)
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS expenses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  vehicle_id INT NOT NULL,
  expense_type VARCHAR(60) NOT NULL,
  cost DECIMAL(10,2) NOT NULL,
  expense_date DATE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);
