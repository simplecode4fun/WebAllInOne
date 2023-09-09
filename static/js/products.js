$(document).ready(function() {
    const countProductOptionSelect = document.getElementById('count_product_option');
    const productForm = document.getElementById('product-form');
    
    
    countProductOptionSelect.addEventListener('change', function() {
        productForm.submit();
    });

    

    
});
// productData = []





document.addEventListener('DOMContentLoaded', function () {
    const productContainer = document.getElementById('product-container');
    let productData = []; // Store your product data here

    function formatPrice(price) {
        const formattedPrice = new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(price);
        return formattedPrice;
    }

    // Function to create a product card
    function createProductCard(product) {
        const card = document.createElement('div');
        card.classList.add('product-card'); // Add your CSS classes here
        // card.style.borderRadius = '6%'
        // Create a div for the product image on the left
        const imageDiv = document.createElement('div');
        imageDiv.classList.add('product-image'); // Add your CSS classes here
        imageDiv.style.width = '60%'; // Thay đổi chiều rộng của imageDiv
        imageDiv.style.display = 'flex'; // Sử dụng flexbox để căn giữa
        imageDiv.style.justifyContent = 'center'; // Căn giữa theo chiều ngang
        imageDiv.style.alignItems = 'center'; // Căn giữa theo chiều dọc
        // imageDiv.style.borderRadius = '50%';
        // Create a link for the product
        const productLink = document.createElement('a');
        productLink.href = product.link;

        // Create the product image
        const productImage = document.createElement('img');
        productImage.src = product.image_link;
        productImage.style.width = '100px';
        productImage.style.height = '125px';
        productImage.style.borderRadius = '0.35rem';

        // Append the image to the link and the link to the imageDiv
        productLink.appendChild(productImage);
        imageDiv.appendChild(productLink);

        // Create a div for the product information on the right
        const infoDiv = document.createElement('div');
        infoDiv.classList.add('product-info');

        // Create h2 and p elements
        const productName = document.createElement('h2');
        const shopName = document.createElement('p');
        const category = document.createElement('p');
        const quantity = document.createElement('p');
        const inventory = document.createElement('p');
        const price = document.createElement('p');
        const totalPrice = document.createElement('p');
        const shopPrice = document.createElement('p');
        const totalPriceShop = document.createElement('p');
        const hr = document.createElement('hr');

        // Populate the text content of the elements
        productName.innerHTML = `<b><a href="${product.link}">${product.product}</a></b>`;
        shopName.innerHTML = `Shop: <a href="${product.shop_link}">${product.shop}</a>`;
        category.innerHTML = `<b>Danh Mục:</b> ${product.category}`;
        quantity.innerHTML = `Số Lượng: ${product.quantity}`;
        inventory.innerHTML = `Tồn Kho: `;
        price.innerHTML = `Giá Mua: ${formatPrice(product.price)}`;
        totalPrice.innerHTML = `Thành Tiền: ${formatPrice(product.price * product.quantity)}`;
        shopPrice.innerHTML = `Giá Shop: ${formatPrice(product.shop_price)}`;
        totalPriceShop.innerHTML = `Thành Tiền Shop: ${formatPrice(product.shop_price * product.quantity)}`;

        // Create an "Edit" button for each element
        function createEditButton() {
            const editButton = document.createElement('button');
            editButton.innerHTML = '<i class="fas fa-edit"></i>';
            editButton.classList.add('edit-button');
            editButton.style.border = "none";
            editButton.style.backgroundColor = "transparent";
            return editButton;
        }

        // Append the "Edit" button after each element
        shopName.appendChild(createEditButton());
        category.appendChild(createEditButton());
        quantity.appendChild(createEditButton());
        price.appendChild(createEditButton());
        totalPrice.appendChild(createEditButton());
        shopPrice.appendChild(createEditButton());
        totalPriceShop.appendChild(createEditButton());

        // Append the elements to the infoDiv
        infoDiv.appendChild(productName);
        infoDiv.appendChild(shopName);
        infoDiv.appendChild(category);
        infoDiv.appendChild(quantity);
        infoDiv.appendChild(inventory);
        infoDiv.appendChild(hr);
        infoDiv.appendChild(price);
        infoDiv.appendChild(totalPrice);
        infoDiv.appendChild(hr);
        infoDiv.appendChild(shopPrice);
        infoDiv.appendChild(totalPriceShop);

        // Create an "Menu" button
        const menuButton = document.createElement('button');
        // menuButton.textContent = 'Menu';
        menuButton.style.width = '10%';
        menuButton.innerHTML = "<i class='fas fa-ellipsis'></i>"
        menuButton.style.backgroundColor = "transparent";
        menuButton.style.border = "none";
        menuButton.style.marginTop = "-35%";
        menuButton.classList.add('menu-button'); // You can style this button using CSS
        menuButton.addEventListener('click', () => {
            // Add your edit functionality here, e.g., open a modal or navigate to an edit page
            // You can access the product data using the `product` object
        });

        
    
        // Append both imageDiv and infoDiv to the main card
        card.appendChild(imageDiv);
        card.appendChild(infoDiv);
        card.appendChild(menuButton);
    
        return card;
    }

    // Function to display product data in cards
    function displayProductData(data) {
        console.log(data);
        productContainer.innerHTML = ''; // Clear previous data
        data.forEach((product) => {
            const card = createProductCard(product);
            productContainer.appendChild(card);
        });
    }

    // Fetch data from the server
    fetch('/productss')
        .then((response) => response.json())
        .then((data) => {
            productData = data.products;
            displayProductData(productData);
        })
        .catch((error) => {
            console.error('Error fetching data:', error);
        });

        // productData = []
        // // Function to update the count information in the HTML
        // function updateCountInfo(countProducts, countOption) {
        //     const countInfoElement = document.getElementById('dataTable_info');
            
        //     // Check if countOption is "ALL"
        //     if (countOption === "ALL") {
        //         countInfoElement.textContent = `Showing 1 to ${countProducts} of ${countProducts} entries`;
        //     } else {
        //         const countOptionInt = parseInt(countOption);
        //         const minCount = Math.min(countOptionInt, countProducts);
        //         countInfoElement.textContent = `Showing 1 to ${minCount} of ${countProducts} entries`;
        //     }
        // }
    
        // function createProductRow(product) {
        //     const row = document.createElement("tr");
        //     row.innerHTML = `
        //         <td>${product.id}</td>
        //         <td>${product.product}</td>
        //         <td>${product.category}</td>
        //         <td>${product.price}</td>
        //         <td>${product.shop_price}</td>
        //         <!-- Add more columns as needed -->
        //     `;
        //     return row;
        //     }
            
        // function displayProductData(data) {
        //     const tableContent = document.getElementById("table-content");
        //     tableContent.innerHTML = '';
        //     console.log(data);
        //     data.forEach((product) => {
        //         const row = createProductRow(product);
        //         tableContent.appendChild(row);
        //     });
        // }
            
        //     // Fetch and display product data
        //     // fetch('/products')
        //     // .then((response) => response.json())
        //     // .then((data) => {
        //     //     productData = data.products;
        //     //     displayProductData(productData);
        //     // });
            
            
        // // Fetch data from the server
        // fetch('/productss')
        // .then(response =>  response.json())
        // .then(data => {
        //     // Sử dụng dữ liệu trong JavaScript
        //     // console.log(data);
        //     productData = data['products'];
    
        //     // Get the count_products and count_product_option values
        //     countProducts = data['count_products']['count_products'];
        //     countOption = data['count_product_option'];
    
        //     // Use the countProducts value to update the HTML
        //     updateCountInfo(countProducts, countOption);
    
        //     // Update the selected option based on count_product_option
        //     countProductOptionSelect.value = countOption;
        //     // console.log(productData);
        //     displayProductData(productData);
        // });
    
        const tableContent = document.getElementById("table-content")
        const tableButtons = document.querySelectorAll(".data-table th button");
        // productData = []
    
        // const productIpTable = document.getElementById("product-ip-table-content")
        // const productIpTableButtons = document.querySelectorAll("#product-ip-table th button");
        // productIPData = []
    
        // const createCreateLinkColumn = (createLinkColumn, obj) => {
    
    
        //     const copyButton = document.createElement("button");
        //     copyButton.innerHTML = '<i class="fa-solid fa-link"></i>';
        //     copyButton.addEventListener("click", () => {
        //         const tempInput = document.createElement("input");
        //         tempInput.value = newUrl;
        //         document.body.appendChild(tempInput);
        //         tempInput.select();
        //         document.execCommand("copy");
        //         document.body.removeChild(tempInput);
        //         // Optionally, you can provide product feedback here
        //     });
    
        //     createLinkColumn.innerHTML = ''; // Clear previous content
        //     // createLinkColumn.appendChild(linkInput);
        //     createLinkColumn.appendChild(copyButton);
        // };
    
        // const createIPListColumn = (ipListColumn, ipList) => {
        //     const showIPButton = document.createElement("button");
        //     showIPButton.innerHTML = '<i class="fa-solid fa-eye"></i>';
            
        //     showIPButton.addEventListener("click", () => {
        //         openProductIpForm();
        //         // Handle the display of IP list here
        //         // You can show a popup or some other UI element to display the list of IPs
        //         // Use the ipList parameter to access the list of IPs for the current product
        //         // For example:
        //         const ipListPopup = document.createElement("div");
        //         ipListPopup.textContent = ipList.join(", "); // Assuming ipList is an array of IP addresses
        //         // Show the popup or update your UI accordingly
        //     });
    
        //     ipListColumn.innerHTML = ''; // Clear previous content
        //     ipListColumn.appendChild(showIPButton);
        // };
    
    
    
        const createRow = (obj) => {
            
            const row = document.createElement("tr");
            const objKeys = Object.keys(obj);
            const columnOrder = ["id", "category", "product", "price", "shop_price", "quantity", "link", "shop", "purchase_date", "receipt_date", "description"];
            // const columnOrder = ["id"]
            columnOrder.forEach((key) => {
                const cell = document.createElement("td");
                const product_id = obj["id"]
                console.log(product_id)
                cell.setAttribute("data-attr", key);
                cell.setAttribute("class", key);
                // cell.innerHTML = obj[key] === null ? "None" : obj[key]; // Handle null values
                cell.innerHTML = obj[key] === null ? "None" : obj[key];
                row.appendChild(cell);
            });
            // const ipListCell = document.createElement("td");
            // createIPListColumn(ipListCell, obj["ip_list"]); // Pass the cell and IP list data to the function
            // row.appendChild(ipListCell);
            
            return row;
        };
    
        // const getTableContent = (data) => {
        //         data.forEach((obj) => {
        //             const row = createProductRow(obj);
        //             tableContent.appendChild(row);
        //         });
        // };
    
        const sortData = (data, param, direction = "asc") => {
            tableContent.innerHTML = '';
            const sortedData = direction == "asc"
                ? [...data].sort(function (a, b) {
                    if (a[param] < b[param]) {
                        return -1;
                    }
                    if (a[param] > b[param]) {
                        return 1;
                    }
                    return 0;
                    })
                : [...data].sort(function (a, b) {
                    if (b[param] < a[param]) {
                        return -1;
                    }
                    if (b[param] > a[param]) {
                        return 1;
                    }
                    return 0;
                });
    
            getTableContent(sortedData);
        };
    
        const resetButtons = (event) => {
            [...tableButtons].map((button) => {
                if (button !== event.target) {
                button.removeAttribute("data-dir");
                }
            });
        };
    
        window.addEventListener("load", () => {
            // console.error (productData)
            // getTableContent(productData);
            
            [...tableButtons].forEach((button) => {
                button.addEventListener("click", (e) => {
                    resetButtons(e);
                    if (e.target.getAttribute("data-dir") === "desc") {
                        sortData(productData, e.target.id, "desc");
                        e.target.setAttribute("data-dir", "asc");
                    } else {
                        sortData(productData, e.target.id, "asc");
                        e.target.setAttribute("data-dir", "desc");
                    }
                });
            });
        });
});