import { Route, Routes } from "react-router-dom";
import ProductList from "./ProductList";
import CreateProduct from "./CreateProduct";
import ProductDetails from "./ProductDetails";
import EditProduct from "./EditProduct";

const Products = () => {
  return (
    <Routes>
      <Route path="/" element={<ProductList />} />
      <Route path="/new" element={<CreateProduct />} />
      <Route path="/:id" element={<ProductDetails />} />
      <Route path="/:id/edit" element={<EditProduct />} />
    </Routes>
  );
};

export default Products;