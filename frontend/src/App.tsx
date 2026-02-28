import { Routes, Route } from "react-router-dom";
import Home from "./pages/home";
import Signup from "./pages/signup";
import Login from "./pages/login";
import Dashboard from "./pages/dashboard";
import PublicRoutes from "./wrappers/PublicRoutes";
import PrivateRoutes from "./wrappers/PrivateRoutes";
import Products from "./pages/products";
import PurchaseOrders from "./pages/purchaseOrders";

const App = () => {
  return (
    <Routes>
      <Route element={<PublicRoutes />}>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
      </Route>
      <Route element={<PrivateRoutes />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/products/*" element={<Products />} />
        <Route path="/purchase-orders/*" element={<PurchaseOrders />} />
      </Route>
    </Routes>
  );
}

export default App;