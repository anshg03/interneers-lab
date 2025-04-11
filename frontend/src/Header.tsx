import React from "react";
import { Link } from "react-router-dom";
import "./Header.css";

const Header: React.FC = () => {
  return (
    <header className="app-header">
      <h1 className="app-title">My Store</h1>
      <nav className="nav-bar">
        <Link to="/">Home</Link>
        <Link to="/products">Products</Link>
      </nav>
    </header>
  );
};

export default Header;
