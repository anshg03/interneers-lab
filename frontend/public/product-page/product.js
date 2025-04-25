fetch("http://127.0.0.1:8001/product/")
  .then((res) => res.json())
  .then((data) => {
    console.log("Fetched products:", data);

    const container = document.getElementById("product-container");

    data.products.forEach((product) => {
      const tile = document.createElement("div");
      tile.className = "product-tile";

      tile.innerHTML = `
        <img src="https://m.media-amazon.com/images/I/71RFdy6y6LL.AC_SX500.jpg" alt="${product.name}" />
        <div class="product-info">
          <h2 class="product-name">${product.name}</h2>
          <p class="product-description">${product.description}</p>
          <p>
          <strong>Brand:</strong> ${product.brand}
          </p>
          <p>
          <strong>Category:</strong> ${product.category}
          </p>
          <p>
          <strong>In Stock:</strong> ${product.quantity}
          </p>
          <p class="product-price">$${product.price}</p>
        </div>
      `;

      container.appendChild(tile);
    });
  })
  .catch((err) => {
    console.error("Failed to fetch products:", err);
  });
