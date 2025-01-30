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
