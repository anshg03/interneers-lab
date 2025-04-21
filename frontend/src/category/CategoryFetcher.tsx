import React, { useEffect, useState } from "react";
import CategoryTile from "./CategoryTile";
import { useNavigate } from "react-router-dom";

type Category = {
  id: string;
  title: string;
  description: string;
  image_url?: string;
};

const CategoryFetcher: React.FC = (): JSX.Element => {
  const [categorys, setCategorys] = useState<Category[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const navigate = useNavigate();
  const queryParameters = new URLSearchParams(window.location.search);
  const page = queryParameters.get("page") || 1;

  useEffect(() => {
    const fetchCategories = async (): Promise<void> => {
      setLoading(true);
      try {
        const res = await fetch(
          `http://127.0.0.1:8001/product/category?page=${page}`,
          {
            method: "GET",
          },
        );
        const data = await res.json();
        console.log("Fetched Categories:", data);
        setCategorys(data.categories);
      } catch (err) {
        console.error("Fetch Error:", err);
      } finally {
        setTimeout(() => setLoading(false), 200);
      }
    };

    fetchCategories();
  }, [page]);

  const handleCreate = async () => {
    const token = localStorage.getItem("user_token");

    if (!token) {
      navigate(`/login?callbackUrl=/create_category`);
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
        navigate("/create_category");
      } else {
        localStorage.removeItem("user_token");
        navigate(`/login?callbackUrl=/create_category`);
      }
    } catch (err) {
      console.error("Token verification failed:", err);
      navigate(`/login?callbackUrl=/create_category`);
    }
  };

  return (
    <div>
      <div
        onClick={handleCreate}
        className="handle-button"
        // style={{ border: "1px solid red" }}
      >
        <button className="create">+ Create</button>
      </div>
      {loading ? (
        <div className="spinner-container">
          <div className="spinner" />
        </div>
      ) : (
        categorys.map((category) => (
          <CategoryTile
            key={category.id}
            id={category.id}
            title={category.title}
            description={category.description}
            imageUrl={
              category.image_url ||
              "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpK1noS9RwpA351YDfG9dRCvSON-j5nZHU0A&s"
            }
          />
        ))
      )}
    </div>
  );
};

export default CategoryFetcher;
