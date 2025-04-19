import React, { useEffect, useState } from "react";
import "./ProductCount.css";
type Product = {
  id: string;
  name: string;
  description: string;
  price: number;
  brand: string;
  category: string;
  quantity: number;
  initial_quantity: number;
  image_url?: string;
};

const Report: React.FC = (): JSX.Element => {
  const [categoryCounts, setCategoryCounts] = useState<Record<string, number>>(
    {},
  );

  const [minPrice, setMinPrice] = useState<number>(0);
  const [maxPrice, setMaxPrice] = useState<number>(1000);
  const [filteredProducts, setFilteredProducts] = useState<Product[]>([]);

  const [lowStockProducts, setLowStockProducts] = useState<Product[]>([]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8001/product/");
        const data = await response.json();
        const products: Product[] = data.products;
        const counts: Record<string, number> = {};
        const lowStock: Product[] = [];

        products.forEach((product) => {
          const categoryName = product.category;
          counts[categoryName] = (counts[categoryName] || 0) + 1;
          const initial = product.initial_quantity;
          const current = product.quantity;
          if (current < 0.1 * initial) {
            lowStock.push(product);
          }
        });

        setCategoryCounts(counts);
        setLowStockProducts(lowStock);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };

    fetchProducts();
  }, []);

  useEffect(() => {
    if (Object.keys(categoryCounts).length > 0 && (window as any).CanvasJS) {
      const dataPoints = Object.entries(categoryCounts).map(
        ([category, count]) => ({
          label: category,
          y: count,
        }),
      );

      const maxi = Math.max(...Object.values(categoryCounts));
      const interval = Math.ceil(maxi / 5) || 1;

      const chart = new (window as any).CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        title: {
          text: "Products per Category",
        },
        axisY: {
          title: "Number of Products",
          interval: interval,
          gridThickness: 0,
        },
        axisX: {
          title: "Category",
        },
        data: [
          {
            type: "column",
            dataPoints,
          },
        ],
      });

      chart.render();
    }
  }, [categoryCounts]);

  const handlePriceSearch = async () => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8001/product/?min_price=${minPrice}&max_price=${maxPrice}`,
      );
      const data = await response.json();
      console.log(data);
      setFilteredProducts(data.products || []);
    } catch (error) {
      console.error("Error fetching products by price:", error);
    }
  };

  return (
    <>
      <div id="chartContainer" className="chart" />
      <div className="results-container">
        <div>
          <div className="price-filter">
            <h2>Filter Products by Price</h2>
            <input
              type="number"
              placeholder="Min Price"
              onChange={(e) => setMinPrice(Number(e.target.value))}
            />
            <input
              type="number"
              placeholder="Max Price"
              onChange={(e) => setMaxPrice(Number(e.target.value))}
            />
            <button onClick={handlePriceSearch}>Search</button>
          </div>

          <div className="filtered-products">
            <h3>Filtered Products</h3>
            {filteredProducts.length > 0 ? (
              <ul>
                {filteredProducts.map((product) => (
                  <li key={product.id}>
                    <strong>{product.name}</strong> - {product.price}
                  </li>
                ))}
              </ul>
            ) : (
              <p>No products found in this range.</p>
            )}
          </div>
        </div>

        <div className="filtered-product">
          <h3>Low Stock Products (Below 10%)</h3>
          {lowStockProducts.length > 0 ? (
            <ul>
              {lowStockProducts.map((product) => (
                <li key={product.id}>
                  <strong>{product.name}</strong> - {product.quantity} left (
                  <strong>Initial</strong> : {product.initial_quantity})
                </li>
              ))}
            </ul>
          ) : (
            <p>No products found in this range.</p>
          )}
        </div>
      </div>
    </>
  );
};

export default Report;
