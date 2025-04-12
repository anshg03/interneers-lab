import React, { useEffect, useState } from "react";
import CategoryTile from "./CategoryTile";

type Category = {
  id: string;
  title: string;
  description: string;
  imageUrl?: string;
};

const CategoryFetcher: React.FC = () => {
  const [categorys, setCategorys] = useState<Category[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchCategories = async (): Promise<void> => {
      setLoading(true);
      try {
        const res = await fetch("http://127.0.0.1:8001/product/category", {
          method: "GET",
        });
        const data = await res.json();
        console.log("Fetched Categories:", data);
        setCategorys(data.categories);
      } catch (err) {
        console.error("Fetch Error:", err);
      } finally {
        // Show spinner for at least 200ms for a better visual cue
        setTimeout(() => setLoading(false), 200);
      }
    };

    fetchCategories();
  }, []);

  return (
    <div>
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
              category.imageUrl ||
              "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpK1noS9RwpA351YDfG9dRCvSON-j5nZHU0A&s"
            }
          />
        ))
      )}
    </div>
  );
};

export default CategoryFetcher;
