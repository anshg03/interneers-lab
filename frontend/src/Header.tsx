import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Header.css";

type HeaderProps = {
  isLoggedIn: boolean;
  setIsLoggedIn: (val: boolean) => void;
};

const Header: React.FC<HeaderProps> = ({ isLoggedIn, setIsLoggedIn }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("user_token");
    setIsLoggedIn(false);
    navigate("/login");
  };

  return (
    <header className="app-header">
      <h1 className="app-title">Inventory</h1>
      <nav className="nav-bar">
        <Link to="/">Home</Link>
        <Link to="/products">Products</Link>
        <Link to="/category">Category</Link>
        <Link to="/reports">Report</Link>
        {isLoggedIn ? (
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        ) : (
          <>
            <Link to="/signup">Signup</Link>
            <Link to="/login">Login</Link>
          </>
        )}
      </nav>
    </header>
  );
};

export default Header;
