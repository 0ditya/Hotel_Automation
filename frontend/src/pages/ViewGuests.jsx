import React, { useEffect, useState } from "react";
import axios from "axios";

export default function ViewGuests() {
  const [guests, setGuests] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5000/admin/guests-data")
      .then(res => setGuests(res.data))
      .catch(err => console.error("Failed to fetch guests", err));
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Guest List</h2>
      <table className="min-w-full bg-white border">
        <thead>
          <tr>
            <th className="px-4 py-2 border">Name</th>
            <th className="px-4 py-2 border">Email</th>
            <th className="px-4 py-2 border">Contact</th>
            <th className="px-4 py-2 border">Frequent</th>
          </tr>
        </thead>
        <tbody>
          {guests.map((guest) => (
            <tr key={guest.id}>
              <td className="px-4 py-2 border">{guest.name}</td>
              <td className="px-4 py-2 border">{guest.email}</td>
              <td className="px-4 py-2 border">{guest.contact}</td>
              <td className="px-4 py-2 border">{guest.is_frequent ? "Yes" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
