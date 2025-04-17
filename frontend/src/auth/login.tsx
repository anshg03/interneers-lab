import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./signup.css";

type UserFormData = {
  username: string;
  password: string;
};

type ToastProps = {
  message: string;
  type?: "success" | "error";
  duration?: number;
};

type LoginProps = {
  setIsLoggedIn: (val: boolean) => void;
};

const Toast: React.FC<ToastProps> = ({
  message,
  type = "success",
  duration = 3000,
}) => {
  const [visible, setVisible] = useState<boolean>(true);

  useEffect(() => {
    const timer = setTimeout(() => setVisible(false), duration);
    return () => clearTimeout(timer);
  }, [duration]);

  return visible ? (
    <div className={`toast ${type}`}>
      <span>{message}</span>
      <div
        className="toast-timer"
        style={{ animationDuration: `${duration}ms` }}
      />
    </div>
  ) : null;
};

const Login: React.FC<LoginProps> = ({ setIsLoggedIn }) => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState<UserFormData>({
    username: "",
    password: "",
  });

  const [showToast, setShowToast] = useState<boolean>(false);
  const [toastMessage, setToastMessage] = useState<string>("");
  const [toastType, setToastType] = useState<"success" | "error">("success");

  const location = useLocation();

  const queryParams = new URLSearchParams(location.search);
  const callbackUrl = queryParams.get("callbackUrl") || "/";

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:8001/product/login", {
        method: "POST",
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      console.log(data);

      if (response.ok) {
        localStorage.setItem("user_token", data.token);
        setIsLoggedIn(true);

        setToastType("success");
        setToastMessage("Successfully logged In!");
        setFormData({
          username: "",
          password: "",
        });
        setTimeout(() => navigate(callbackUrl), 3000);
      } else {
        setToastType("error");
        setToastMessage("Failed to login, invalid credentials.");
      }
    } catch (error) {
      setToastType("error");
      setToastMessage("Something went wrong. Please try again.");
    } finally {
      setShowToast(true);
    }
  };

  return (
    <div className="signup-container">
      <form onSubmit={handleSubmit} className="signup-form">
        <h1>Login</h1>
        <h4>Welcome Back!</h4>
        <h3>Login to your account</h3>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          required
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
          minLength={5}
        />

        <button type="submit">Login</button>

        <div>
          Don't have an account?{" "}
          <span onClick={() => navigate("/signup")} className="click">
            Signup
          </span>
        </div>
        {showToast && <Toast message={toastMessage} type={toastType} />}
      </form>
    </div>
  );
};

export default Login;
