import { Route, Routes } from "react-router-dom";
import PurchaseOrderList from "./PurchaseOrderList";
import PurchaseOrderDetails from "./PurchaseOrderDetails";
import CreatePurchaseOrder from "./CreatePurchaseOrder";
import EditPurchaseOrder from "./EditPurchaseOrder";

const Products = () => {
  return (
    <Routes>
      <Route path="/" element={<PurchaseOrderList />} />
      <Route path="/new" element={<CreatePurchaseOrder />} />
      <Route path="/:id" element={<PurchaseOrderDetails />} />
      <Route path="/:id/edit" element={<EditPurchaseOrder />} />
    </Routes>
  );
};

export default Products;