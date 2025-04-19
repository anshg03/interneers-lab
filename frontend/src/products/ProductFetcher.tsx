import React, { useEffect, useState } from "react";
import ProductTile from "./ProductTile";
import "./CategoryFilter.css";
import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";

type Product = {
  id: string;
  name: string;
  description: string;
  price: number;
  brand: string;
  category: string;
  quantity: number;
  image_url?: string;
};

type Category = {
  id: string;
  title: string;
};

const ProductFetcher: React.FC = (): JSX.Element => {
  const navigate = useNavigate();
  const location = useLocation();

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
        console.log(data.products);
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
        setFilteredProducts(Array.isArray(data) && data.length > 0 ? data : []);
      }
    } catch (err) {
      console.error(`Failed to fetch products for ${category}:`, err);
    } finally {
      setTimeout(() => setLoading(false), 500);
    }
  };

  const handleCreate = async () => {
    const token = localStorage.getItem("user_token");

    if (!token) {
      navigate(`/login?callbackUrl=/create`);
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
        navigate("/create");
      } else {
        localStorage.removeItem("user_token");
        navigate(`/login?callbackUrl=/create`);
      }
    } catch (err) {
      console.error("Token verification failed:", err);
      navigate(`/login?callbackUrl=/create`);
    }
  };

  return (
    <div>
      <div className="Btw">
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
        {location.pathname === "/products" && (
          <div onClick={handleCreate}>
            <button className="create">+ Create</button>
          </div>
        )}
      </div>

      {loading ? (
        <div className="spinner-container">
          <div className="spinner" />
        </div>
      ) : filteredProducts.length === 0 ? (
        <p className="no-products-message">
          Oops! No products in this category.
        </p>
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
              product.image_url ??
              "https://cdn.oreillystatic.com/oreilly/images/device-image4-800x600-20210224.jpg"
            }
            currentPath={location.pathname}
          />
        ))
      )}
    </div>
  );
};

export default ProductFetcher;
