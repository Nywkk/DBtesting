// Function to fetch products from the server
async function fetchProducts() {
    try {
        const response = await fetch('/api/products'); // Replace '/products' with the appropriate endpoint
        const products = await response.json();
        return products;
    } catch (error) {
        console.error('Error fetching products:', error);
        return [];
    }
}

// Function to display products on the page
function displayProducts(products) {
    const productContainer = document.getElementById('productContainer');

    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.classList.add('product-card');

        productCard.innerHTML = `
            <img src="/static/${product.image}" alt="${product.name}" class="product-image">
            <div class="product-name">${product.name}</div>
            <div class="product-price">$${parseFloat(product.price).toFixed(2)}</div>
            <div class="product-description">${product.description}</div>
        `;

        productContainer.appendChild(productCard);
    });
}


// Fetch products and display them when the page loads
window.onload = async () => {
    const products = await fetchProducts();
    displayProducts(products);
};



// Function to handle form submission
function submitForm(event) {
    event.preventDefault();
    var formData = new FormData(this);
    
    fetch('/users', {
        method: 'POST',
        body: JSON.stringify(Object.fromEntries(formData)),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').innerText = data.message || data.error;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Add event listener to form submission
document.getElementById('userForm').addEventListener('submit', submitForm);
