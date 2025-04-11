import React, { useEffect, useState } from "react";
import ProductTile from "./ProductTile";
import "./CategoryFilter.css";

type Product = {
  id: string;
  name: string;
  description: string;
  price: number;
  brand: string;
  category: string;
  quantity: number;
  imageUrl?: string;
};

type Category = {
  id: string;
  title: string;
};

const ProductFetcher = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [filteredProducts, setFilteredProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>("");

  useEffect(() => {
    fetch("http://127.0.0.1:8001/product/", {
      method: "GET",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Fetched Products:", data);
        setProducts(data.products);
        setFilteredProducts(data.products);
      })
      .catch((err) => console.error("Fetch Error:", err));

    fetch("http://127.0.0.1:8001/product/category")
      .then((res) => res.json())
      .then((data) => setCategories(data.categories))
      .catch((err) => console.error("Fetch Categories Error:", err));
  }, []);

  const handleCategoryChange = async (
    e: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    const category = e.target.value;
    console.log(category);
    setSelectedCategory(category);

    if (category === "") {
      setFilteredProducts(products);
    } else {
      try {
        const res = await fetch(
          `http://127.0.0.1:8001/product/product_from_category_name/${category}/`,
        );
        const data = await res.json();
        console.log(data);
        const fetched = Array.isArray(data) ? data : [data];
        setFilteredProducts(fetched);
      } catch (err) {
        console.error(`Failed to fetch products for ${category}:`, err);
      }
    }
  };

  return (
    <div>
      <div className="category-filter-container">
        <label htmlFor="categoryFilter" className="category-filter-label">
          Filter by Category:
        </label>
        <select
          id="categoryFilter"
          value={selectedCategory}
          onChange={handleCategoryChange}
          className="category-filter-select"
        >
          <option value="">All</option>
          {categories.map((cat) => (
            <option key={cat.id} value={cat.title}>
              {cat.title}
            </option>
          ))}
        </select>
      </div>

      {filteredProducts.map((product, index) => (
        <ProductTile
          key={index}
          id={product.id}
          name={product.name}
          description={product.description}
          price={`${product.price}`}
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
