// BillViewPage.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";

const BillViewPage = () => {
  const [bill, setBill] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`http://127.0.0.1:5000/guest/bill?guest_id=1`)
      .then((res) => {
        console.log("💰 Bill data:", res.data);
        setBill(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("❌ Failed to fetch bill:", err);
        setError("Failed to load bill");
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading bill...</p>;
  if (error) return <p>{error}</p>;
  if (!bill) return <p>No bill found</p>;

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Your Bill</h2>
      <p className="text-xl mb-2">Total Amount: ₹ {bill.totalAmount}</p>
      <p>Status: {bill.isPaid ? "Paid" : "Pending"}</p>
      <a
        href="http://127.0.0.1:5000/guest/bill/download"
        className="mt-4 inline-block px-4 py-2 bg-blue-500 text-white rounded"
      >
        Download PDF
      </a>
    </div>
  );
};

export default BillViewPage;

