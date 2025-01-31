const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileElem");
const fileName = document.getElementById("file-name");

// Click to select file
dropArea.addEventListener("click", () => fileInput.click());

// Show selected file name
fileInput.addEventListener("change", function () {
    fileName.textContent = this.files.length > 0 ? this.files[0].name : "No file chosen";
});

// Drag & Drop
dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.style.border = "2px solid #00ff00";
});

dropArea.addEventListener("dragleave", () => {
    dropArea.style.border = "2px dashed #555";
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.style.border = "2px dashed #555";

    if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        fileName.textContent = e.dataTransfer.files[0].name;
    }
});

document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent default form submission
    uploadFile(); // Call the function when the form is submitted
    console.log("Got here (Prevent reload)")
});

function uploadFile() {
    const fileInput = document.getElementById('fileElem');  // File input element
    const errorContainer = document.getElementById('errorContainer');  // Error message container
    const successContainer = document.getElementById('successContainer');  // Success message container

    if (fileInput.files.length === 0) {
        showAlert(errorContainer, "Please select a file to upload!", "danger");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/api/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showAlert(errorContainer, data.error, "danger", "Error");  // Show error message
        } else {
            showAlert(successContainer, "File uploaded successfully!", "success", "Success");
            setTimeout(() => {
                window.location.href = "/results";  // Redirect to results page
            }, 2000);
        }
    })
    .catch(error => {
        showAlert(errorContainer, "Upload failed. Try again.", "danger", "Error");
        console.error("Upload Error:", error);
    });
}

// Function to display Bootstrap alert messages with SVG icons
function showAlert(container, message, type, hint) {
    const icons = {
        success: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-check-circle-fill me-2" viewBox="0 0 16 16">
                    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-2.03a.75.75 0 0 0-1.06 0L7.75 9.19l-1.72-1.72a.75.75 0 1 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.06 0l4.25-4.25a.75.75 0 0 0 0-1.06"/>
                  </svg>`,
        danger: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-exclamation-triangle-fill me-2" viewBox="0 0 16 16">
                    <path d="M7.938 2.016a1.13 1.13 0 0 1 2.125 0l6.857 11.885c.457.793-.091 1.8-1.063 1.8H2.063c-.972 0-1.52-1.007-1.063-1.8L7.937 2.016zm.562 4.98a.905.905 0 0 0-.9.9v2.4a.905.905 0 0 0 1.8 0v-2.4a.905.905 0 0 0-.9-.9zm.9 6a.9.9 0 1 0-1.8 0 .9.9 0 0 0 1.8 0"/>
                  </svg>`,
        warning: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-exclamation-circle-fill me-2" viewBox="0 0 16 16">
                    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM7.002 5.5a.905.905 0 0 1 1.8 0v3.6a.905.905 0 0 1-1.8 0V5.5zm1.003 6.905a.9.9 0 1 1-1.8 0 .9.9 0 0 1 1.8 0"/>
                  </svg>`
    };

    container.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show p-3" role="alert">
            ${icons[type] || ""} <strong style="font-weight: 500">${hint}:</strong><span class="ms-1">${message}</span>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}
