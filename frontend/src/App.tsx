import React from "react";
import { Routes, Route } from "react-router-dom";
import "./App.css";
import Header from "./Header";
import ProductFetcher from "./products/ProductFetcher";
import CreateProduct from "products/ProductCreate";
import CategoryFetcher from "category/CategoryFetcher";
import CreateCategory from "category/CategoryCreate";

const App: React.FC = () => {
  return (
    <div className="App">
      <Header />
      <Routes>
        <Route path="/" element={<ProductFetcher />} />
        <Route path="/products" element={<ProductFetcher />} />
        <Route path="/create" element={<CreateProduct />} />
        <Route path="/create_category" element={<CreateCategory />} />
        <Route path="/category" element={<CategoryFetcher />} />
      </Routes>
    </div>
  );
};

export default App;
