function triggerFileInput() {
    document.getElementById('imageInput').click();
}

function uploadImage() {
    const input = document.getElementById('imageInput');
    const file = input.files[0];

    if (!file) {
        alert('Please select an image.');
        return;
    }

    // Resize the image to 150x150 using a canvas
    const reader = new FileReader();
    reader.onload = function(event) {
        const img = new Image();
        img.onload = function() {
            const canvas = document.createElement('canvas');
            canvas.width = 150;
            canvas.height = 150;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, 150, 150);

            canvas.toBlob(function(blob) {
                const formData = new FormData();
                formData.append('file', blob, file.name);
                formData.append('target_width', '200');
                formData.append('target_height', '200');

                fetch('http://192.168.1.132:8088/process-image/', { // Replace with your API endpoint
                        method: 'POST',
                        body: formData
                    })
                    .then(response => {
                        console.log('Response Status:', response.status);
                        if (!response.ok) {
                            throw new Error('Network response was not ok ' + response.statusText);
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log('API Response:', data);
                        displayResult(blob, data);
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        displayResult(blob, { error: 'No Response' });
                    });
            }, 'image/jpeg');
        }
        img.src = event.target.result;
    }
    reader.readAsDataURL(file);
}

function displayResult(file, data) {
    const img = document.getElementById('uploadedImage');
    const responseText = document.getElementById('apiResponse');
    const resultDiv = document.getElementById('result');
    const thumbnailsDiv = document.getElementById('thumbnails');

    img.src = URL.createObjectURL(file);
    img.style.display = 'block';
    responseText.textContent = data.error ? data.error : 'API Call Successful';

    resultDiv.style.display = 'block';

    // Clear any previous thumbnails
    thumbnailsDiv.innerHTML = '<h3>Generated Images</h3>';

    if (data.stacked_images) {
        data.stacked_images.forEach((imageArray, index) => {
            // Validate imageData structure
            if (!Array.isArray(imageArray)) {
                console.error(`Invalid imageData structure for image ${index + 1}`);
                return;
            }

            // Convert nested arrays to base64
            const base64Image = arrayToBase64(imageArray);

            // Display thumbnail
            const imgElement = document.createElement('img');
            imgElement.src = base64Image;
            imgElement.alt = `Generated Image ${index + 1}`;
            imgElement.style.margin = '5px';
            imgElement.style.border = '1px solid #ddd';
            imgElement.style.borderRadius = '4px';
            imgElement.style.maxWidth = '80px';
            imgElement.style.maxHeight = '80px';
            thumbnailsDiv.appendChild(imgElement);
        });
    } else {
        thumbnailsDiv.innerHTML += '<p>No Images Generated</p>';
    }
}

function arrayToBase64(imageArray) {
    // Convert nested arrays to flat array of pixels
    let flattenedPixels = [];
    imageArray.forEach(row => {
        row.forEach(pixel => {
            flattenedPixels.push(...pixel);
        });
    });

    // Convert to Uint8ClampedArray for ImageData
    const width = imageArray[0].length; // Assuming all rows have the same length
    const height = imageArray.length;
    const pixels = new Uint8ClampedArray(flattenedPixels);

    // Create ImageData object and draw on canvas
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');
    const imageDataObj = ctx.createImageData(width, height);

    // Fill ImageData with pixel data
    for (let i = 0; i < pixels.length; i += 4) {
        imageDataObj.data[i] = pixels[i]; // Red channel
        imageDataObj.data[i + 1] = pixels[i + 1]; // Green channel
        imageDataObj.data[i + 2] = pixels[i + 2]; // Blue channel
        imageDataObj.data[i + 3] = 255; // Alpha channel
    }

    ctx.putImageData(imageDataObj, 0, 0);

    // Convert canvas to base64 image
    const base64Image = canvas.toDataURL('image/jpeg');

    return base64Image;
}