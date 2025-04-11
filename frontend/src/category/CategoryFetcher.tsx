import React, { useEffect, useState } from "react";
import CategoryTile from "./CategoryTile";

type Category = {
  id: string;
  title: string;
  description: string;
  imageUrl?: string;
};

const CategoryFetcher = () => {
  const [categorys, setCategorys] = useState<Category[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8001/product/category", {
      method: "GET",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Fetched Categorys:", data);
        setCategorys(data.categories);
      })
      .catch((err) => console.error("Fetch Error:", err));
  }, []);

  return (
    <div>
      {categorys.map((category, index) => (
        <CategoryTile
          key={index}
          id={category.id}
          title={category.title}
          description={category.description}
          imageUrl="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpK1noS9RwpA351YDfG9dRCvSON-j5nZHU0A&s"
        />
      ))}
    </div>
  );
};

export default CategoryFetcher;
