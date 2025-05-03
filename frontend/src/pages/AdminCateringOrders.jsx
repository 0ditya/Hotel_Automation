import React, { useEffect, useState } from "react";
import axios from "axios";

export default function AdminCateringOrders() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5000/admin/catering-orders-data")
      .then((res) => setOrders(res.data))
      .catch((err) => console.error("Failed to fetch catering orders", err));
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Catering Orders</h2>
      {orders.length === 0 ? (
        <p>No orders found.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border">
            <thead>
              <tr>
                <th className="px-4 py-2 border">Order ID</th>
                <th className="px-4 py-2 border">Guest Name</th>
                <th className="px-4 py-2 border">Items</th>
                <th className="px-4 py-2 border">Total</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.id}>
                  <td className="px-4 py-2 border">{order.id}</td>
                  <td className="px-4 py-2 border">{order.guestName}</td>
                  <td className="px-4 py-2 border">
                    <ul>
                      {order.items.map((item, i) => (
                        <li key={i}>{item.name} × {item.quantity}</li>
                      ))}
                    </ul>
                  </td>
                  <td className="px-4 py-2 border">₹ {order.total}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}