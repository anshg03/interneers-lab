import React, { useState, useEffect } from "react";
import "./ProductCreate.css";

type ProductFormData = {
  name: string;
  description: string;
  price: string;
  brand: string;
  category: string;
  quantity: string;
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

const CreateProduct: React.FC = () => {
  const [formData, setFormData] = useState<ProductFormData>({
    name: "",
    description: "",
    price: "",
    brand: "",
    category: "",
    quantity: "",
  });

  const [showToast, setShowToast] = useState<boolean>(false);
  const [toastMessage, setToastMessage] = useState<string>("");
  const [toastType, setToastType] = useState<"success" | "error">("success");

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ): void => {
    const { name, value } = e.target;
    setFormData((prev: ProductFormData) => ({
      ...prev,
      [name]: value,
    }));
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
          price: parseFloat(formData.price),
          quantity: parseInt(formData.quantity),
        }),
      });

      const data = await response.json();
      console.log(data);

      if (response.ok) {
        setToastType("success");
        setToastMessage("Successfully created the product!");
        setFormData({
          name: "",
          description: "",
          price: "",
          brand: "",
          category: "",
          quantity: "",
        });
      } else {
        setToastType("error");
        setToastMessage("Failed to create product.");
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
      <h2>Create New Product</h2>

      <input
        name="name"
        placeholder="Product Name"
        value={formData.name}
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
      <input
        name="price"
        type="number"
        placeholder="Price"
        value={formData.price}
        onChange={handleChange}
        required
      />
      <input
        name="brand"
        placeholder="Brand"
        value={formData.brand}
        onChange={handleChange}
        required
      />
      <input
        name="category"
        placeholder="Category"
        value={formData.category}
        onChange={handleChange}
        required
      />
      <input
        name="quantity"
        type="number"
        placeholder="Quantity"
        value={formData.quantity}
        onChange={handleChange}
        required
      />
      <button type="submit">Create Product</button>

      {showToast && <Toast message={toastMessage} type={toastType} />}
    </form>
  );
};

export default CreateProduct;
