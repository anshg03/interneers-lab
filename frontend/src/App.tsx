import React from "react";
import { Routes, Route } from "react-router-dom";
import "./App.css";
import Header from "./Header";
import ProductFetcher from "./products/ProductFetcher";
import CreateProduct from "products/ProductCreate";

const App: React.FC = () => {
  return (
    <div className="App">
      <Header />
      <Routes>
        <Route path="/" element={<ProductFetcher />} />
        <Route path="/products" element={<ProductFetcher />} />
        <Route path="/create" element={<CreateProduct />} />
        <Route path="/create_category" element={<CreateProduct />} />
      </Routes>
    </div>
  );
};

export default App;
