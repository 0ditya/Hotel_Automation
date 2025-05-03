import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import GuestDashboard from "./pages/GuestDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import RoomReservationPage from "./pages/RoomReservationPage";
import BillViewPage from "./pages/BillViewPage";
import FoodOrderPage from "./pages/FoodOrderPage";
import AdminCateringOrders from "./pages/AdminCateringOrders";
import ManageRooms from "./pages/ManageRooms";
import ViewGuests from "./pages/ViewGuests";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/guest/dashboard" element={<GuestDashboard />} />
        <Route path="/admin/dashboard" element={<AdminDashboard />} />
        <Route path="/guest/reserve" element={<RoomReservationPage />} />
        <Route path="/guest/bill" element={<BillViewPage />} />
        <Route path="/guest/food" element={<FoodOrderPage />} />
        <Route path="/admin/catering-orders" element={<AdminCateringOrders />} />
        <Route path="/admin/rooms" element={<ManageRooms />} />
        <Route path="/admin/guests" element={<ViewGuests />} />
        <Route path="*" element={<h1 className="p-4 text-center">404 - Page Not Found</h1>} />
      </Routes>
    </Router>
  );
}
export default App;