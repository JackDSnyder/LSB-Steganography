document.addEventListener('DOMContentLoaded', function() {
    // Helper function to show/hide loading spinner
    function toggleLoading(button, isLoading) {
        const spinner = button.querySelector('.spinner-border');
        if (isLoading) {
            spinner.classList.remove('d-none');
            button.disabled = true;
        } else {
            spinner.classList.add('d-none');
            button.disabled = false;
        }
    }

    // Helper function to create download button with timestamp
    function createDownloadButton(fileUrl, fileName) {
        const timestamp = new Date().getTime();
        return `
            <a href="${fileUrl}?t=${timestamp}" download="${fileName}" class="btn btn-success mt-2">
                <i class="bi bi-download"></i> Download ${fileName}
            </a>
        `;
    }

    // Helper function to create image URL with timestamp
    function createImageUrl(fileUrl) {
        const timestamp = new Date().getTime();
        return `${fileUrl}?t=${timestamp}`;
    }

    // Helper function to reset form
    function resetForm(formId) {
        const form = document.getElementById(formId);
        if (form) {
            form.reset();
        }
    }

    // Helper function to create a download link
    function createDownloadLink(blob, filename) {
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.className = 'btn btn-primary mt-3';
        link.textContent = 'Download Result';
        return link;
    }

    // Helper function to create an image element
    function createImageElement(blob) {
        const url = URL.createObjectURL(blob);
        const img = document.createElement('img');
        img.src = url;
        img.className = 'img-fluid mt-3';
        img.alt = 'Result';
        return img;
    }

    // Text Encoding
    const textEncodeForm = document.getElementById('textEncodeForm');
    const textEncodeResult = document.getElementById('textEncodeResult');
    const encodeTextBtn = document.getElementById('encodeText');

    textEncodeForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        toggleLoading(encodeTextBtn, true);
        textEncodeResult.innerHTML = ''; // Clear previous results
        
        const formData = new FormData();
        formData.append('image', document.getElementById('textImage').files[0]);
        formData.append('text', document.getElementById('message').value);
        formData.append('password', document.getElementById('textPassword').value);

        try {
            const response = await fetch('/encode-text', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                // Get the blob from the response
                const blob = await response.blob();
                // Create a URL for the blob
                const imageUrl = URL.createObjectURL(blob);
                
                textEncodeResult.innerHTML = `
                    <div class="alert alert-success">
                        Text encoded successfully!
                    </div>
                    <img src="${imageUrl}" class="result-image" alt="Encoded image">
                    <a href="${imageUrl}" download="encoded_image.png" class="btn btn-success mt-2">
                        <i class="bi bi-download"></i> Download encoded_image.png
                    </a>
                `;
                resetForm('textEncodeForm'); // Reset form after success
            } else {
                const data = await response.json();
                textEncodeResult.innerHTML = `
                    <div class="alert alert-danger">
                        ${data.error}
                    </div>
                `;
            }
        } catch (error) {
            textEncodeResult.innerHTML = `
                <div class="alert alert-danger">
                    An error occurred while encoding the text.
                </div>
            `;
        } finally {
            toggleLoading(encodeTextBtn, false);
        }
    });

    // Text Decoding
    const textDecodeForm = document.getElementById('textDecodeForm');
    const textDecodeResult = document.getElementById('textDecodeResult');
    const decodeTextBtn = document.getElementById('decodeText');

    textDecodeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData();
        
        // Get the file input and password input
        const imageFile = document.getElementById('textDecodeImage').files[0];
        const password = document.getElementById('textDecodePassword').value;
        
        // Add the file and password to formData
        formData.append('image', imageFile);
        formData.append('password', password);
        
        const submitButton = e.target.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
        textDecodeResult.innerHTML = ''; // Clear previous results

        try {
            const response = await fetch('/decode-text', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Decoding failed');
            }

            if (data.error) {
                textDecodeResult.innerHTML = `<div class="alert alert-danger">Error: ${data.error}</div>`;
            } else if (data.text === '') {
                textDecodeResult.innerHTML = '<div class="alert alert-warning">No text found in the image.</div>';
            } else {
                textDecodeResult.innerHTML = `
                    <div class="alert alert-success">Text decoded successfully!</div>
                    <div class="mt-3">
                        <h5>Decoded Text:</h5>
                        <p class="border p-3 bg-light">${data.text}</p>
                    </div>
                `;
            }
            resetForm('textDecodeForm');
        } catch (error) {
            textDecodeResult.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = 'Decode Text';
        }
    });

    // Image Encoding
    const imageEncodeForm = document.getElementById('imageEncodeForm');
    const imageEncodeResult = document.getElementById('imageEncodeResult');
    const encodeImageBtn = document.getElementById('encodeImage');

    imageEncodeForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        toggleLoading(encodeImageBtn, true);
        imageEncodeResult.innerHTML = ''; // Clear previous results
        
        const formData = new FormData();
        formData.append('original', document.getElementById('originalImage').files[0]);
        formData.append('hidden', document.getElementById('hiddenImage').files[0]);
        formData.append('password', document.getElementById('imagePassword').value);

        try {
            const response = await fetch('/encode-image', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                // Get the blob from the response
                const blob = await response.blob();
                // Create a URL for the blob
                const imageUrl = URL.createObjectURL(blob);
                
                imageEncodeResult.innerHTML = `
                    <div class="alert alert-success">
                        Image encoded successfully!
                    </div>
                    <img src="${imageUrl}" class="result-image" alt="Encoded image">
                    <a href="${imageUrl}" download="encoded_image.png" class="btn btn-success mt-2">
                        <i class="bi bi-download"></i> Download encoded_image.png
                    </a>
                `;
                resetForm('imageEncodeForm'); // Reset form after success
            } else {
                const data = await response.json();
                imageEncodeResult.innerHTML = `
                    <div class="alert alert-danger">
                        ${data.error}
                    </div>
                `;
            }
        } catch (error) {
            imageEncodeResult.innerHTML = `
                <div class="alert alert-danger">
                    An error occurred while encoding the image.
                </div>
            `;
        } finally {
            toggleLoading(encodeImageBtn, false);
        }
    });

    // Image Decoding
    const imageDecodeForm = document.getElementById('imageDecodeForm');
    const imageDecodeResult = document.getElementById('imageDecodeResult');
    const decodeImageBtn = document.getElementById('decodeImage');

    imageDecodeForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        toggleLoading(decodeImageBtn, true);
        imageDecodeResult.innerHTML = ''; // Clear previous results
        
        const formData = new FormData();
        formData.append('image', document.getElementById('imageDecodeInput').files[0]);
        formData.append('password', document.getElementById('imageDecodePassword').value);

        try {
            const response = await fetch('/decode-image', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                // Get the blob from the response
                const blob = await response.blob();
                // Create a URL for the blob
                const imageUrl = URL.createObjectURL(blob);
                
                imageDecodeResult.innerHTML = `
                    <div class="alert alert-success">
                        Image decoded successfully!
                    </div>
                    <img src="${imageUrl}" class="result-image" alt="Decoded image">
                    <a href="${imageUrl}" download="decoded_image.png" class="btn btn-success mt-2">
                        <i class="bi bi-download"></i> Download decoded_image.png
                    </a>
                `;
                resetForm('imageDecodeForm'); // Reset form after success
            } else {
                const data = await response.json();
                imageDecodeResult.innerHTML = `
                    <div class="alert alert-danger">
                        ${data.error}
                    </div>
                `;
            }
        } catch (error) {
            imageDecodeResult.innerHTML = `
                <div class="alert alert-danger">
                    An error occurred while decoding the image.
                </div>
            `;
        } finally {
            toggleLoading(decodeImageBtn, false);
        }
    });
}); 