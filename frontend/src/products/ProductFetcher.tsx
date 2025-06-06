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

const ProductFetcher: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [filteredProducts, setFilteredProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const res = await fetch("http://127.0.0.1:8001/product/");
        const data = await res.json();
        setProducts(data.products || []);
        setFilteredProducts(data.products || []);

        const categoryRes = await fetch(
          "http://127.0.0.1:8001/product/category",
        );
        const categoryData = await categoryRes.json();
        setCategories(categoryData.categories || []);
      } catch (err) {
        console.error("Fetch Error:", err);
      } finally {
        setTimeout(() => setLoading(false), 500);
      }
    };

    fetchData();
  }, []);

  const handleCategoryChange = async (
    e: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    const category = e.target.value;
    setSelectedCategory(category);
    setLoading(true);

    try {
      if (category === "") {
        setFilteredProducts(products);
      } else {
        const res = await fetch(
          `http://127.0.0.1:8001/product/product_from_category_name/${category}/`,
        );
        const data = await res.json();
        const fetched = Array.isArray(data) ? data : [data];
        setFilteredProducts(fetched);
      }
    } catch (err) {
      console.error(`Failed to fetch products for ${category}:`, err);
    } finally {
      setTimeout(() => setLoading(false), 500);
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

      {loading ? (
        <div className="spinner-container">
          <div className="spinner" />
        </div>
      ) : (
        filteredProducts.map((product) => (
          <ProductTile
            key={product.id}
            id={product.id}
            name={product.name}
            description={product.description}
            price={`${product.price}`}
            brand={product.brand}
            category={product.category}
            quantity={product.quantity}
            imageUrl={
              product.imageUrl ??
              "https://cdn.oreillystatic.com/oreilly/images/device-image4-800x600-20210224.jpg"
            }
          />
        ))
      )}
    </div>
  );
};

export default ProductFetcher;
