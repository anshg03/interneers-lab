import React from "react";
import "./ProductTile.css";

type ProductTileProps = {
  name: string;
  description: string;
  price: string;
  brand: string;
  category: string;
  quantity: number;
  imageUrl: string;
};

const ProductTile: React.FC<ProductTileProps> = ({
  name,
  description,
  price,
  imageUrl,
  brand,
  category,
  quantity,
}) => {
  return (
    <div className="product-tile">
      <img className="product-image" src={imageUrl} alt={name} />
      <div className="product-info">
        <h2 className="product-name">{name}</h2>
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
        <button className="buy-button">Buy Now</button>
      </div>
    </div>
  );
};

export default ProductTile;
