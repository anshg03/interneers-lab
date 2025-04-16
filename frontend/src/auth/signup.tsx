import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
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
const Signup: React.FC = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState<UserFormData>({
    username: "",
    password: "",
  });

  const [showToast, setShowToast] = useState<boolean>(false);
  const [toastMessage, setToastMessage] = useState<string>("");
  const [toastType, setToastType] = useState<"success" | "error">("success");

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:8001/product/signup", {
        method: "POST",
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      console.log(data);

      if (response.ok) {
        setToastType("success");
        setToastMessage("Successfully account created!");
        setFormData({
          username: "",
          password: "",
        });
        setTimeout(() => navigate("/login"), 3000);
      } else {
        setToastType("error");
        setToastMessage("Failed to create account.");
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
        <h1>Signup</h1>
        <h3>Create Your Account</h3>
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

        <button type="submit">Signup</button>
        {showToast && <Toast message={toastMessage} type={toastType} />}
      </form>
    </div>
  );
};

export default Signup;
