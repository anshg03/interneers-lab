import React from "react";
import "./ProductTile.css";

type ProductTileProps = {
  name: string;
  description: string;
  price: string;
  imageUrl: string;
};

const ProductTile: React.FC<ProductTileProps> = ({
  name,
  description,
  price,
  imageUrl,
}) => {
  return (
    <div className="product-tile">
      <img className="product-image" src={imageUrl} alt={name} />
      <div className="product-info">
        <h2 className="product-name">{name}</h2>
        <p className="product-description">{description}</p>
        <p className="product-price">{price}</p>
        <button className="buy-button">Buy Now</button>
      </div>
    </div>
  );
};

export default ProductTile;
