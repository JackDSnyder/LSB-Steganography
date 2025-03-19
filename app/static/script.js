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
            const data = await response.json();
            
            if (data.success) {
                const imageUrl = createImageUrl('/static/uploads/' + data.output_file);
                textEncodeResult.innerHTML = `
                    <div class="alert alert-success">
                        Text encoded successfully!
                    </div>
                    <img src="${imageUrl}" class="result-image" alt="Encoded image">
                    ${createDownloadButton('/static/uploads/' + data.output_file, 'encoded_image.png')}
                `;
                resetForm('textEncodeForm'); // Reset form after success
            } else {
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

    textDecodeForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        toggleLoading(decodeTextBtn, true);
        textDecodeResult.innerHTML = ''; // Clear previous results
        
        const formData = new FormData();
        formData.append('image', document.getElementById('textDecodeImage').files[0]);
        formData.append('password', document.getElementById('textDecodePassword').value);

        try {
            const response = await fetch('/decode-text', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            
            if (data.success) {
                textDecodeResult.innerHTML = `
                    <div class="alert alert-success">
                        Decoded text: ${data.text}
                    </div>
                `;
                resetForm('textDecodeForm'); // Reset form after success
            } else {
                textDecodeResult.innerHTML = `
                    <div class="alert alert-danger">
                        ${data.error}
                    </div>
                `;
            }
        } catch (error) {
            textDecodeResult.innerHTML = `
                <div class="alert alert-danger">
                    An error occurred while decoding the text.
                </div>
            `;
        } finally {
            toggleLoading(decodeTextBtn, false);
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
            const data = await response.json();
            
            if (data.success) {
                const imageUrl = createImageUrl('/static/uploads/' + data.output_file);
                imageEncodeResult.innerHTML = `
                    <div class="alert alert-success">
                        Image encoded successfully!
                    </div>
                    <img src="${imageUrl}" class="result-image" alt="Encoded image">
                    ${createDownloadButton('/static/uploads/' + data.output_file, 'encoded_image.png')}
                `;
                resetForm('imageEncodeForm'); // Reset form after success
            } else {
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
            const data = await response.json();
            
            if (data.success) {
                const imageUrl = createImageUrl('/static/uploads/' + data.output_file);
                imageDecodeResult.innerHTML = `
                    <div class="alert alert-success">
                        Image decoded successfully!
                    </div>
                    <img src="${imageUrl}" class="result-image" alt="Decoded image">
                    ${createDownloadButton('/static/uploads/' + data.output_file, 'decoded_image.png')}
                `;
                resetForm('imageDecodeForm'); // Reset form after success
            } else {
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