import React, { useState, useEffect } from "react";
import "./ProductTile.css";

type ProductTileProps = {
  id: string;
  name: string;
  description: string;
  price: string;
  brand: string;
  category: string;
  quantity: number;
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

const ProductTile: React.FC<ProductTileProps> = ({
  id,
  name,
  description,
  price,
  imageUrl,
  brand,
  category,
  quantity,
}) => {
  const [expanded, setExpanded] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState("");
  const [toastType, setToastType] = useState<"success" | "error">("success");
  const [formData, setFormData] = useState({
    name,
    description,
    price,
    brand,
    category,
    quantity,
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
    fetch(`http://127.0.0.1:8001/product/update/${id}/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        ...formData,
        price: parseFloat(formData.price),
        quantity: parseInt(formData.quantity.toString()),
      }),
    })
      .then(async (res) => {
        const data = await res.json();

        if (res.ok) {
          setToastType("success");
          setToastMessage("Successfully updated the product!");
          closeModal();
        } else {
          setToastType("error");
          setToastMessage(data?.message || "Failed to update product.");
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
        <img className="product-image" src={imageUrl} alt={name} />
        <div className="product-info">
          <h2 className="product-name">{name}</h2>

          {expanded && (
            <div className="product-details">
              <p className="product-description">{description}</p>
              <p>
                <strong>Brand:</strong> {brand}
              </p>
              <p>
                <strong>Category:</strong> {category}
              </p>
              <p>
                <strong>In Stock:</strong> {quantity}
              </p>
              <p className="product-price">{price}</p>
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
                <label htmlFor="name">Name:</label>
                <input
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                />
              </div>

              <div className="form-row">
                <label htmlFor="price">Price:</label>
                <input
                  id="price"
                  name="price"
                  value={formData.price}
                  onChange={handleChange}
                />
              </div>

              <div className="form-row">
                <label htmlFor="brand">Brand:</label>
                <input
                  id="brand"
                  name="brand"
                  value={formData.brand}
                  onChange={handleChange}
                />
              </div>

              <div className="form-row">
                <label htmlFor="category">Category:</label>
                <input
                  id="category"
                  name="category"
                  value={formData.category}
                  onChange={handleChange}
                />
              </div>

              <div className="form-row">
                <label htmlFor="quantity">Quantity:</label>
                <input
                  id="quantity"
                  name="quantity"
                  value={formData.quantity}
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

export default ProductTile;
