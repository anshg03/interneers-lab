import React from "react";
import { BrowserRouter as Routes, Route } from "react-router-dom";
import "./App.css";
import Header from "./Header";
import ProductFetcher from "./ProductFetcher";

function App() {
  return (
    <div className="App">
      <Header />
      <Routes>
        <Route path="/" element={<ProductFetcher />} />
        <Route path="/products" element={<ProductFetcher />} />
        <Route path="/contact" element={<ProductFetcher />} />
      </Routes>
    </div>
  );
}

export default App;
