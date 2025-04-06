import React from "react";
import "./App.css";
import ProductTile from "./ProductTile";

function App() {
  return (
    <div className="App">
      <ProductTile
        name="Wireless Headphones"
        description="High-quality sound, long battery life, and sleek design."
        price="$99.99"
        imageUrl="https://m.media-amazon.com/images/I/71RFdy6y6LL.AC_SX500.jpg"
      />
    </div>
  );
}

export default App;
