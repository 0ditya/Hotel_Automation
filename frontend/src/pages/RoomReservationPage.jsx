import React, { useState, useEffect } from "react";
import axios from "axios";

const RoomReservationPage = () => {
  const [formData, setFormData] = useState({
    room_id: "",
    checkin_date: "",
    checkout_date: "",
    advance_paid: "",
  });
  const [message, setMessage] = useState("");
  const [rooms, setRooms] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/admin/rooms-data", { withCredentials: true })
      .then((res) => {
        setRooms(res.data);
      })
      .catch((err) => {
        console.error("Error fetching rooms:", err);
      });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const response = await axios.post("http://localhost:5000/guest/reserve", formData, {
        withCredentials: true,
      });

      if (response.data.success) {
        setMessage("Reservation successful!");
        setFormData({
          room_id: "",
          checkin_date: "",
          checkout_date: "",
          advance_paid: "",
        });
      } else {
        setMessage("Failed: " + response.data.message);
      }
    } catch (err) {
      console.error("Reservation error:", err);
      setMessage("An error occurred while making the reservation.");
    }
  };

  return (
    <div className="p-6 max-w-lg mx-auto bg-white rounded-xl shadow-md space-y-4">
      <h2 className="text-2xl font-semibold">Reserve a Room</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <select
          name="room_id"
          value={formData.room_id}
          onChange={handleChange}
          required
          className="w-full p-2 border rounded"
        >
          <option value="">Select Room</option>
          {rooms.map((room) => (
            <option key={room.id} value={room.id}>
              Room {room.room_number} - {room.room_type} - ₹{room.current_tariff}
            </option>
          ))}
        </select>

        <input
          type="date"
          name="checkin_date"
          value={formData.checkin_date}
          onChange={handleChange}
          required
          className="w-full p-2 border rounded"
        />
        <input
          type="date"
          name="checkout_date"
          value={formData.checkout_date}
          onChange={handleChange}
          required
          className="w-full p-2 border rounded"
        />
        <input
          name="advance_paid"
          placeholder="Advance Amount"
          type="number"
          value={formData.advance_paid}
          onChange={handleChange}
          required
          className="w-full p-2 border rounded"
        />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Submit Reservation
        </button>
      </form>
      {message && <p className="text-center text-red-500">{message}</p>}
    </div>
  );
};

export default RoomReservationPage;