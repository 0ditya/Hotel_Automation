// frontend/src/pages/AdminDashboard.js
import React from 'react';
import { Link } from 'react-router-dom';

export default function AdminDashboard() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Admin Dashboard</h1>
      <ul className="space-y-3">
        <li><Link to="/admin/rooms" className="text-blue-600">Manage Rooms</Link></li>
        <li><Link to="/admin/guests" className="text-blue-600">View Guests</Link></li>
        <li><Link to="/admin/catering-orders" className="text-blue-600">View Food Orders</Link></li>
      </ul>
    </div>
  );
}
