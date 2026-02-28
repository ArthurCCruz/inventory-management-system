import { Route, Routes } from "react-router-dom";
import SaleOrderDetails from "./SaleOrderDetails";
import CreateSaleOrder from "./CreateSaleOrder";
import EditSaleOrder from "./EditSaleOrder";
import SaleOrderList from "./SaleOrderList";

const SaleOrders = () => {
  return (
    <Routes>
      <Route path="/" element={<SaleOrderList />} />
      <Route path="/new" element={<CreateSaleOrder />} />
      <Route path="/:id" element={<SaleOrderDetails />} />
      <Route path="/:id/edit" element={<EditSaleOrder />} />
    </Routes>
  );
};

export default SaleOrders;