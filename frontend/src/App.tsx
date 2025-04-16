import React, { useEffect, useState } from "react";
import { Routes, Route } from "react-router-dom";
import "./App.css";
import Header from "./Header";
import ProductFetcher from "./products/ProductFetcher";
import CreateProduct from "products/ProductCreate";
import CategoryFetcher from "category/CategoryFetcher";
import CreateCategory from "category/CategoryCreate";
import Signup from "auth/signup";
import Login from "auth/login";

const App: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("user_token");
    setIsLoggedIn(!!token);
  }, []);

  return (
    <div className="App">
      <Header isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
      <Routes>
        <Route path="/" element={<ProductFetcher />} />
        <Route path="/products" element={<ProductFetcher />} />
        <Route path="/create" element={<CreateProduct />} />
        <Route path="/create_category" element={<CreateCategory />} />
        <Route path="/category" element={<CategoryFetcher />} />
        <Route path="/signup" element={<Signup />} />
        <Route
          path="/login"
          element={<Login setIsLoggedIn={setIsLoggedIn} />}
        />
      </Routes>
    </div>
  );
};

export default App;
