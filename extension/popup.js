document.addEventListener('DOMContentLoaded', function() {
    const checkBtn = document.getElementById('checkBtn');
    const resultDiv = document.getElementById('result');
    const urlDisplay = document.getElementById('urlDisplay');

    // Get the current tab's URL and display it
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        const currentUrl = tabs[0].url;
        urlDisplay.textContent = currentUrl.length > 40 ? currentUrl.substring(0, 37) + '...' : currentUrl;
    });

    checkBtn.addEventListener('click', function() {
        resultDiv.textContent = 'Analyzing...';
        resultDiv.className = '';

        // Get the URL of the currently active tab
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            const urlToCheck = tabs[0].url;

            // Send the URL to our Flask API
            fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: urlToCheck })
            })
            .then(response => response.json())
            .then(data => {
                // Update the popup with the prediction
                resultDiv.textContent = `Result: ${data.prediction}`;
                if (data.prediction === 'Phishing') {
                    resultDiv.className = 'phishing';
                } else {
                    resultDiv.className = 'legitimate';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                resultDiv.textContent = 'Error: API is offline.';
                resultDiv.className = 'phishing';
            });
        });
    });
});