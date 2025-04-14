import React, { useState, useEffect } from "react";
import "./CategoryCreate.css";

type CategoryFormData = {
  title: string;
  description: string;
  image: File | null;
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

const CreateCategory: React.FC = (): JSX.Element => {
  const [formData, setFormData] = useState<CategoryFormData>({
    title: "",
    description: "",
    image: null,
  });

  const [showToast, setShowToast] = useState<boolean>(false);
  const [toastMessage, setToastMessage] = useState<string>("");
  const [toastType, setToastType] = useState<"success" | "error">("success");

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ): void => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
    const file = e.target.files?.[0] ?? null;
    setFormData((prev) => ({ ...prev, image: file }));
  };

  const handleSubmit = async (
    e: React.FormEvent<HTMLFormElement>,
  ): Promise<void> => {
    e.preventDefault();

    const form = new FormData();
    form.append("title", formData.title);
    form.append("description", formData.description);
    if (formData.image) {
      form.append("image", formData.image);
    }
    console.log(formData);
    try {
      const response = await fetch(
        "http://127.0.0.1:8001/product/category/create/",
        {
          method: "POST",
          body: form,
        },
      );

      const data = await response.json();
      console.log(data);

      if (response.ok) {
        setToastType("success");
        setToastMessage("Successfully created the category!");
        setFormData({ title: "", description: "", image: null });
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
      <input type="file" accept="image/*" onChange={handleImageChange} />

      <button type="submit">Create Category</button>

      {showToast && <Toast message={toastMessage} type={toastType} />}
    </form>
  );
};

export default CreateCategory;
