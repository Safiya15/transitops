# TransitOps

TransitOps is a full-stack Transport Operations Management System developed during an 8-hour hackathon. The platform digitizes transport operations by enabling organizations to efficiently manage vehicles, drivers, trips, maintenance, fuel expenses, and operational analytics from a centralized dashboard.

#Live demo
https://transitops-sigma.vercel.app/

**Backend API:** https://transitops-production-b49f.up.railway.app

## Project Overview

Many transport and logistics companies still rely on spreadsheets and manual processes for fleet management. TransitOps addresses this challenge by providing a centralized web application that simplifies vehicle management, driver allocation, trip scheduling, maintenance tracking, and expense monitoring while enforcing important business rules.

## Features

### Authentication
- Secure user authentication using email and password
- Role-Based Access Control (RBAC)
- Protected routes for authenticated users

### Dashboard
- Active Vehicles
- Available Vehicles
- Vehicles in Maintenance
- Active Trips
- Pending Trips
- Drivers on Duty
- Fleet Utilization

### Vehicle Management
- Register and manage vehicles
- Update vehicle details
- Track vehicle status
- Unique vehicle registration validation

### Driver Management
- Manage driver information
- License validation
- Safety score tracking
- Driver availability management

### Trip Management
- Create and manage trips
- Assign available drivers and vehicles
- Cargo weight validation
- Automatic status transitions

### Maintenance Management
- Create maintenance records
- Automatically update vehicle status
- Prevent vehicles under maintenance from being assigned

### Fuel & Expense Management
- Record fuel logs
- Track maintenance expenses
- Calculate operational costs

### Reports & Analytics
- Fleet utilization
- Fuel efficiency
- Operational cost analysis
- Vehicle performance insights

## Business Rules

- Vehicle registration numbers must be unique.
- Vehicles under maintenance cannot be assigned to trips.
- Drivers with expired licenses or suspended status cannot be assigned.
- Vehicles and drivers already on a trip cannot be assigned again.
- Cargo weight cannot exceed the vehicle's maximum capacity.
- Completing or cancelling a trip automatically updates vehicle and driver availability.
- Creating a maintenance record automatically marks the vehicle as "In Shop."

## Tech Stack

### Frontend
- React.js
- React Router
- Axios
- CSS

### Backend
- Node.js
- Express.js

### Database
- MySQL

### Deployment
- Frontend: Vercel
- Backend: Railway
- Database: Railway MySQL

## Project Structure

```
TransitOps
│
├── frontend
│   ├── css
│   ├── js
    html files

│  
│
├── backend
│   ├── routes
│   ├── controllers
│   ├── middleware
│   ├── db.js
│   ├── server.js
│   └── package.json
│
└── README.md
```

## Installation

### Clone the repository

```bash
git clone https://github.com/Safiya15/transitops.git
cd transitops
```

### Backend Setup

```bash
cd backend
npm install
```

Create a `.env` file:

```env
DB_HOST=your_host
DB_PORT=your_port
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
JWT_SECRET=your_secret
```

Start the backend server:

```bash
npm start
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Deployment

The application is deployed using:

- Frontend: Vercel
- Backend: Railway
- Database: Railway MySQL

## Future Enhancements

- CSV and PDF report export
- Email reminders for license expiry
- Vehicle document management
- Advanced analytics dashboard
- Search, filtering, and sorting
- Dark mode support
- Real-time notifications



## Team

This project was developed during an 8-hour hackathon as a collaborative team project.

## License

This project was developed for educational and hackathon purposes.
