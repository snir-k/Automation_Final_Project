/**
 * PRODUCT MANAGEMENT SYSTEM - EXTERNAL JAVASCRIPT CONTROLLER ENGINE
 * Hardened to handle short HHMM timestamps, precise regex stripping, and table sync.
 * Cleaned from redundant local variable declarations and malformed JavaScript variables.
 */

// Global variable to track if the uploader form is currently in "Edit Mode"
let currentEditingProductId = null;

// Autoload inventory data blocks as soon as the DOM compile environment is ready
document.addEventListener('DOMContentLoaded', loadProducts);

// Global event listener to intercept form submissions safely without inline deprecated HTML attributes
document.addEventListener('DOMContentLoaded', () => {
    const productForm = document.getElementById('product-form');
    if (productForm) {
        productForm.addEventListener('submit', handleFormSubmission);
    }
});



// Global event listener to intercept file uploader mutations across jpg, png, jpeg targets
const fileUploader = document.getElementById('file-uploader');
if (fileUploader) {
    fileUploader.addEventListener('change', function(event) {
        // FIXES BUG: Safe file metadata assignment checking array bounds to prevent crashes
        if (event.target.files && event.target.files.length > 0) {
            document.getElementById('product-image').value = event.target.files[0].name;
        }
    });
}

/**
 * Native JavaScript controller function to successfully close the modal card stack safely
 */
function closeProductDetails() {
    const detailsCard = document.getElementById('product-details');
    if (detailsCard) {
        detailsCard.style.display = 'none';
    }
}

/**
 * Dynamic rendering engine to query Flask GET backend and populate the UI table grid
 */
async function loadProducts() {
    const tbody = document.getElementById('table-body');
    if (!tbody) return;
    tbody.innerHTML = '';

    try {
        const response = await fetch('/api/products');
        const products = await response.json();

        products.forEach(p => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${p.product_id}</td>
                <td>${p.name}</td>
                <td>$${parseFloat(p.price).toFixed(2)}</td>
                <td>${p.image || 'None'}</td>
                <td>
                    <button class="btn btn-info" onclick="showProductDetails('${p.product_id}', '${p.name}', '${p.price}', '${p.image}')">Details</button>
                    <button class="btn btn-warning" style="background-color: #ffc107; color: #000; border: 1px solid #ffc107; padding: 6px 12px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-right: 5px;" onclick="startEditProduct('${p.product_id}', '${p.name}', '${p.price}', '${p.image}')">Edit</button>
                    <button class="btn btn-danger" onclick="deleteProduct('${p.product_id}')">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (err) {
        console.error("Failed to parse localized inventory metrics.", err);
    }
}

/**
 * Robust image element generation that builds verified source bindings
 * FIXES BUG: Maps directly to the absolute web asset serving folder path correctly
 */
function showProductDetails(id, name, price, image) {
    document.getElementById('details-id').innerText = id;
    document.getElementById('details-name').innerText = name;
    document.getElementById('details-price').innerText = parseFloat(price).toFixed(2);

    const imgContainer = document.getElementById('details-image-container');

    if (image && image.trim() !== "" && image !== 'None' && image !== 'null') {
        // FIXES PATH RECONCILIATION: Strips any leading slash to avoid broken absolute routing paths
        const normalizedPath = image.startsWith('/') ? image.substring(1) : image;
        imgContainer.innerHTML = `
            <img src="/static/${normalizedPath}" 
                 alt="${name}" 
                 style="max-width: 180px; height: auto; border-radius: 4px; border: 1px solid #ccc; display: block; margin-top: 10px;">
        `;
    } else {
        imgContainer.innerHTML = '<span style="color: grey; font-style: italic;">No image artifact attached to this product resource</span>';
    }
    document.getElementById('product-details').style.display = 'block';
}

/**
 * TRANSITION LAYER: Populates the input form fields with existing data to allow user mutations (Edit Mode)
 */
function startEditProduct(id, name, price, image) {
    currentEditingProductId = id;

    // FIXES BUG: Loads the name exactly as it is in the table to preserve the original timestamp structure
    document.getElementById('product-name').value = name;
    document.getElementById('product-price').value = price;

    // Trims path literals directly to populate input interface fields cleanly
    document.getElementById('product-image').value = image.replace(/^uploads\//, '');

    // Smooth scroll navigation to bring the form interface focus up to the user viewport
    document.getElementById('product-form').scrollIntoView({ behavior: 'smooth' });
}

/**
 * ASYNC FORM SUBMISSION CORE: Leverages FormData across both POST and PUT pipelines to handle file binaries cleanly.
 * FIXES BUG #11 & BUG #13: Validates raw whitespace injection blocks and enforces strict image schema extensions.
 */
async function handleFormSubmission(event) {
    event.preventDefault();
    const alertBox = document.getElementById('ui-alert-box');
    if (alertBox) alertBox.style.display = 'none';

    const inputName = document.getElementById('product-name').value;
    const price = document.getElementById('product-price').value;
    const imageInput = document.getElementById('product-image').value;
    const fileInput = document.getElementById('file-uploader');

    // FIXES BUG #12 (Upper Bound Validation): Intercept numeric overflow chains dynamically on client-side
    if (price && parseFloat(price) > 9999999) {
        if (alertBox) {
            alertBox.className = "alert alert-error";
            alertBox.innerText = "Error: Product price exceeds maximum structural limit of \$9,999,999.";
            alertBox.style.display = 'block';
        }
        return;
    }

    // REGEX VALIDATION GATES: Enforces strict secure whitelist alphanumeric criteria and image extensions
    // FIXES BUG #11 & #13: Strict Alphanumeric starter and clean end-anchor expression
    const imageRegex = /^[a-zA-Z0-9][a-zA-Z0-9_\-\s.]*\.(png|jpg|jpeg)$/i;



    // INTERCEPT FOR EDIT OPERATIONS (HARDENED MULTIPART PUT PIPELINE)
    if (currentEditingProductId !== null) {
        // Validate Product Name in Edit Mode
        if (!inputName || inputName.trim() === "" || inputName.trim().length < 2) {
            if (alertBox) {
                alertBox.className = "alert alert-error";
                alertBox.innerText = "Error: Product name must be at least 2 characters long and cannot consist of spaces only.";
                alertBox.style.display = 'block';
            }
            return;
        }

        // FIXES BUG #13: Validate Image Filename/Extension in Edit Mode
        if (imageInput && imageInput.trim() !== "" && !imageRegex.test(imageInput.trim())) {
            if (alertBox) {
                alertBox.className = "alert alert-error";
                alertBox.innerText = "Error: Invalid image filename format. Only letters, numbers, dashes, and standard extensions (.png, .jpg, .jpeg) are permitted.";
                alertBox.style.display = 'block';
            }
            return;
        }

        try {
            const formDataPUT = new FormData();
            formDataPUT.append('name', inputName);
            formDataPUT.append('price', price);
            formDataPUT.append('image', imageInput);

            if (fileInput && fileInput.files && fileInput.files.length > 0) {
                formDataPUT.append('file', fileInput.files[0]);
            }

            const response = await fetch(`/api/products/${currentEditingProductId}`, {
                method: 'PUT',
                body: formDataPUT
            });

            if (response.ok) {
                alertBox.className = "alert alert-success";
                alertBox.innerText = "Success: Product state updated and synchronized in database and file cluster!";
                alertBox.style.display = 'block';
                currentEditingProductId = null;
                document.getElementById('product-form').reset();
                closeProductDetails();
                await loadProducts();
            } else {
                const result = await response.json();
                alertBox.className = "alert alert-error";
                alertBox.innerText = `Error: ${result.error || "Update cycle rejected"}`;
                alertBox.style.display = 'block';
            }
        } catch (err) {
            console.error("PUT execution link error.", err);
        }
        return;
    }

    // ORIGINAL POST PIPELINE ROUTING FOR CREATING NEW RESOURCES
    // Validate Product Name
    if (!inputName || inputName.trim() === "" || inputName.trim().length < 2) {
        if (alertBox) {
            alertBox.className = "alert alert-error";
            alertBox.innerText = "Error: Product name must be at least 2 characters long and cannot consist of spaces only.";
            alertBox.style.display = 'block';
        }
        return;
    }

    // FIXES BUG #13 (Payload Security Bound): Checks if the image filename meets validation criteria BEFORE submission
    if (imageInput && imageInput.trim() !== "" && !imageRegex.test(imageInput.trim())) {
        if (alertBox) {
            alertBox.className = "alert alert-error";
            alertBox.innerText = "Error: Invalid image filename format. Only letters, numbers, dashes, and standard extensions (.png, .jpg, .jpeg) are permitted.";
            alertBox.style.display = 'block';
        }
        return;
    }

    // UX UPGRADE: Generates a clean 4-digit HHMM dynamic timestamp for new items
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const shortTimestamp = `${hours}${minutes}`;

    const nameWithTimestamp = `${inputName.trim()} ${shortTimestamp}`;

    const formData = new FormData();
    formData.append('name', nameWithTimestamp);
    formData.append('price', price);
    formData.append('image', imageInput.trim());

    if (fileInput && fileInput.files && fileInput.files.length > 0) {
        formData.append('file', fileInput.files[0]);
    }

    try {
        const response = await fetch('/api/products', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            alertBox.className = "alert alert-success";
            alertBox.innerText = "Success: Product file compiled and persisted to database and server directory!";
            alertBox.style.display = 'block';
            document.getElementById('product-form').reset();
            await loadProducts();
        } else {
            alertBox.className = "alert alert-error";
            alertBox.innerText = `Error: ${result.error || "Dataset checkpoint rejected"}`;
            alertBox.style.display = 'block';
        }
    } catch (err) {
        alertBox.className = "alert alert-error";
        alertBox.innerText = "Critical: Connection broken or server checkpoint offline.";
        alertBox.style.display = 'block';
    }
}


/**
 * Native client execution logic to trigger resource deletion loops via standard API endpoints
 */
async function deleteProduct(id) {
    if (confirm("Are you sure you want to delete this product?")) {
        try {
            const response = await fetch(`/api/products/${id}`, { method: 'DELETE' });
            if (response.ok) {
                closeProductDetails();
                await loadProducts();
            }
        } catch (err) {
            console.error("Delete operation checkpoint aborted.", err);
        }
    }
}
