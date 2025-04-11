import React, { useState, useEffect } from "react";
import "./CategoryTile.css";

type CategoryTileProps = {
  id: string;
  title: string;
  description: string;
  imageUrl: string;
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
    <div className="toast">
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
}) => {
  const [expanded, setExpanded] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState("");
  const [toastType, setToastType] = useState<"success" | "error">("success");
  const [formData, setFormData] = useState({
    title,
    description,
  });

  const handleToggle = () => setExpanded(!expanded);
  const openModal = () => setShowModal(true);
  const closeModal = () => setShowModal(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = () => {
    fetch(`http://127.0.0.1:8001/product/category/update/${id}/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        ...formData,
      }),
    })
      .then(async (res) => {
        const data = await res.json();

        if (res.ok) {
          setToastType("success");
          setToastMessage("Successfully updated the category!");
          closeModal();
        } else {
          setToastType("error");
          setToastMessage(data?.message || "Failed to update category.");
        }

        setShowToast(true);
      })
      .catch((err) => {
        console.error("Update failed:", err);
        setToastType("error");
        setToastMessage("Something went wrong. Please try again.");
        setShowToast(true);
      });
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
            <h3>Edit Product</h3>
            <div className="modal-form">
              <div className="form-row">
                <label htmlFor="name">Title:</label>
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
