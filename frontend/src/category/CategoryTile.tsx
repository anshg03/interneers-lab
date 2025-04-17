import React, { useState, useEffect } from "react";
import "./CategoryTile.css";
import { useNavigate } from "react-router-dom";

type CategoryTileProps = {
  id: string;
  title: string;
  description: string;
  imageUrl: string;
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

const CategoryTile: React.FC<CategoryTileProps> = ({
  id,
  title,
  description,
  imageUrl,
}): JSX.Element => {
  const [expanded, setExpanded] = useState<boolean>(false);
  const [showModal, setShowModal] = useState<boolean>(false);
  const [showToast, setShowToast] = useState<boolean>(false);
  const [toastMessage, setToastMessage] = useState<string>("");
  const [toastType, setToastType] = useState<"success" | "error">("success");

  const navigate = useNavigate();
  const [formData, setFormData] = useState<{
    title: string;
    description: string;
  }>({
    title,
    description,
  });

  const handleToggle = (): void => setExpanded((prev) => !prev);
  const openModal = async () => {
    const token = localStorage.getItem("user_token");

    if (!token) {
      navigate(`/login?callbackUrl=/category`);
      return;
    }

    try {
      const response = await fetch(
        "http://127.0.0.1:8001/product/verify-token",
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );
      if (response.ok) {
        setShowModal(true);
      } else {
        localStorage.removeItem("user_token");
        navigate(`/login?callbackUrl=/category`);
      }
    } catch (err) {
      console.error("Token verification failed:", err);
      navigate(`/login?callbackUrl=/category`);
    }
  };
  const closeModal = (): void => setShowModal(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ): void => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (): Promise<void> => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8001/product/category/update/${id}/`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        },
      );

      const data = await response.json();

      if (response.ok) {
        setToastType("success");
        setToastMessage("Successfully updated the category!");
        closeModal();
      } else {
        setToastType("error");
        setToastMessage(data?.message || "Failed to update category.");
      }
    } catch (error) {
      console.error("Update failed:", error);
      setToastType("error");
      setToastMessage("Something went wrong. Please try again.");
    } finally {
      setShowToast(true);
    }
  };

  return (
    <>
      <div
        className={`product-tile ${expanded ? "expanded" : ""}`}
        onClick={handleToggle}
      >
        <img className="product-image" src={imageUrl} alt={title} />
        <div className="product-info">
          <h2 className="product-name">{title}</h2>

          {expanded && (
            <div className="product-details">
              <p className="product-description">{description}</p>
              <button className="buy-button" onClick={openModal}>
                Update Details
              </button>
            </div>
          )}
        </div>
      </div>

      {showModal && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Edit Category</h3>
            <div className="modal-form">
              <div className="form-row">
                <label htmlFor="title">Title:</label>
                <input
                  id="title"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                />
              </div>

              <div className="form-row">
                <label htmlFor="description">Description:</label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="modal-buttons">
              <button onClick={handleSubmit}>Confirm</button>
              <button onClick={closeModal}>Cancel</button>
            </div>
          </div>
        </div>
      )}

      {showToast && <Toast message={toastMessage} type={toastType} />}
    </>
  );
};

export default CategoryTile;
