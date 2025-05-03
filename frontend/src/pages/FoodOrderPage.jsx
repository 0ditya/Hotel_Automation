import React, { useEffect, useState } from "react";
import axios from "axios";
axios.get("http://localhost:5000/api/guest/food-menu", {
  withCredentials: true
})
.then(res => setMenu(res.data))
.catch(err => console.error("Failed to fetch menu", err));

export default function FoodOrderPage() {
  const [menu, setMenu] = useState([]);
  const [quantities, setQuantities] = useState({});

  useEffect(() => {
    axios
      .get("http://localhost:5000/api/guest/food-menu")
      .then((res) => setMenu(res.data))
      .catch((err) => {
        console.error("Failed to fetch menu", err);
        alert("Could not load menu items");
      });
  }, []);

  const handleQuantityChange = (itemID, value) => {
    setQuantities((prev) => ({
      ...prev,
      [itemID]: parseInt(value) || 0,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const orderItems = menu
      .filter((item) => quantities[item.itemID] > 0)
      .map((item) => ({
        itemID: item.itemID,
        name: item.name,
        quantity: quantities[item.itemID],
        price: item.price,
      }));

    if (orderItems.length === 0) {
      alert("Please select at least one item.");
      return;
    }

    try {
      const res = await axios.post("http://localhost:5000/api/guest/food-order", {
        items: orderItems,
      });
      if (res.data.success) {
        alert("Order placed successfully!");
        setQuantities({});
      } else {
        alert("Failed to place order");
      }
    } catch (err) {
      console.error("Order error:", err);
      alert("Order submission failed");
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Order Food</h2>
      {menu.length === 0 ? (
        <p>No menu items found.</p>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          {menu.map((item) => (
            <div key={item.itemID} className="flex justify-between items-center">
              <span>
                {item.name} - ₹{item.price}
              </span>
              <input
                type="number"
                min="0"
                value={quantities[item.itemID] || ""}
                onChange={(e) => handleQuantityChange(item.itemID, e.target.value)}
                className="w-20 border px-2 py-1 rounded"
              />
            </div>
          ))}
          <button
            type="submit"
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          >
            Submit Order
          </button>
        </form>
      )}
    </div>
  );
}
