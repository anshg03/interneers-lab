import React, { useState, useEffect } from "react";
import "./CategoryCreate.css";

type CategoryFormData = {
  title: string;
  description: string;
};

const Toast: React.FC<{
  message: string;
  type?: "success" | "error";
  duration?: number;
}> = ({ message, type = "success", duration = 3000 }) => {
  const [visible, setVisible] = useState(true);

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

const CreateCategory: React.FC = () => {
  const [formData, setFormData] = useState<CategoryFormData>({
    title: "",
    description: "",
  });

  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState("");
  const [toastType, setToastType] = useState<"success" | "error">("success");

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:8001/product/create/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ...formData,
        }),
      });

      const data = await response.json();
      console.log(data);
      if (response.ok) {
        setToastType("success");
        setToastMessage("Successfully created the category!");
        setFormData({
          title: "",
          description: "",
        });
      } else {
        setToastType("error");
        setToastMessage("Failed to create category.");
      }
    } catch (error) {
      setToastType("error");
      setToastMessage("Something went wrong. Please try again.");
    } finally {
      setShowToast(true);
    }
  };

  return (
    <form className="create-product-form" onSubmit={handleSubmit}>
      <h2>Create New Category</h2>

      <input
        name="title"
        placeholder="Category Name"
        value={formData.title}
        onChange={handleChange}
        required
      />
      <textarea
        name="description"
        placeholder="Description"
        value={formData.description}
        onChange={handleChange}
        required
      />

      <button type="submit">Create Category</button>

      {showToast && <Toast message={toastMessage} type={toastType} />}
    </form>
  );
};

export default CreateCategory;
