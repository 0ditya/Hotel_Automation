// frontend/src/pages/GuestDashboard.js
import React from 'react';
import { Link } from 'react-router-dom';

export default function GuestDashboard() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Guest Dashboard</h1>
      <ul className="space-y-3">
        <li><Link to="/guest/reserve" className="text-blue-600">Reserve a Room</Link></li>
        <li><Link to="/guest/food" className="text-blue-600">Order Food</Link></li>
        <li><Link to="/guest/bill" className="text-blue-600">View Bill</Link></li>
      </ul>
    </div>
  );
}
