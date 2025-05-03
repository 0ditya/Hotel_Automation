import React, { useEffect, useState } from "react";
import axios from "axios";

export default function ManageRooms() {
  const [rooms, setRooms] = useState([]);
  const [reservations, setReservations] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5000/admin/rooms-data")
      .then((response) => {setRooms(response.data)})
      .catch(err => console.error("Failed to fetch rooms", err));

    axios.get("http://localhost:5000/admin/reservations-data")
      .then(res => setReservations(res.data))
      .catch(err => console.error("Failed to fetch reservations", err));
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Manage Rooms</h2>

      <h3 className="text-xl font-semibold mb-2">Room Inventory</h3>
      <table className="min-w-full bg-white border mb-6">
        <thead>
          <tr>
            <th className="px-4 py-2 border">Room No</th>
            <th className="px-4 py-2 border">Type</th>
            <th className="px-4 py-2 border">AC</th>
            <th className="px-4 py-2 border">Tariff</th>
            <th className="px-4 py-2 border">Occupied</th>
          </tr>
        </thead>
        <tbody>
          {rooms.map((room) => (
            <tr key={room.room_number}>
              <td className="px-4 py-2 border">{room.room_number}</td>
              <td className="px-4 py-2 border">{room.room_type}</td>
              <td className="px-4 py-2 border">{room.is_ac ? "Yes" : "No"}</td>
              <td className="px-4 py-2 border">₹ {room.current_tariff}</td>
              <td className="px-4 py-2 border">{room.is_occupied ? "Yes" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3 className="text-xl font-semibold mb-2">Recent Reservations</h3>
      <table className="min-w-full bg-white border">
        <thead>
          <tr>
            <th className="px-4 py-2 border">Guest Name</th>
            <th className="px-4 py-2 border">Room</th>
            <th className="px-4 py-2 border">Check In</th>
            <th className="px-4 py-2 border">Check Out</th>
            <th className="px-4 py-2 border">Advance</th>
          </tr>
        </thead>
        <tbody>
          {reservations.map((res) => (
            <tr key={res.id}>
              <td className="px-4 py-2 border">{res.guest_name}</td>
              <td className="px-4 py-2 border">{res.room_number}</td>
              <td className="px-4 py-2 border">{res.check_in}</td>
              <td className="px-4 py-2 border">{res.check_out}</td>
              <td className="px-4 py-2 border">₹ {res.advance_paid}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}