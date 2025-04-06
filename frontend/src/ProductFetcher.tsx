import React, { useEffect, useState } from "react";
import ProductTile from "./ProductTile";

type Product = {
  name: string;
  description: string;
  price: number;
  brand: string;
  category: string;
  quantity: number;
  imageUrl?: string;
};

const ProductFetcher = () => {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8001/product/")
      .then((res) => res.json())
      .then((data) => {
        console.log("Fetched Products:", data);
        setProducts(data.products);
      })
      .catch((err) => console.error("Fetch Error:", err));
  }, []);

  return (
    <div>
      {products.map((product, index) => (
        <ProductTile
          key={index}
          name={product.name}
          description={product.description}
          price={`$${product.price}`}
          brand={product.brand}
          category={product.category}
          quantity={product.quantity}
          imageUrl="https://cdn.oreillystatic.com/oreilly/images/device-image4-800x600-20210224.jpg"
        />
      ))}
    </div>
  );
};

export default ProductFetcher;
