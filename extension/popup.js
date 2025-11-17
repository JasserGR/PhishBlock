document.addEventListener('DOMContentLoaded', function() {
    const resultCard = document.getElementById('result-card');
    const resultText = document.getElementById('result-text');
    const resultIcon = document.getElementById('result-icon');
    const resultMessage = document.getElementById('result-message');
    const urlDisplay = document.getElementById('urlDisplay');
    const loader = document.getElementById('loader');

    function analyzeCurrentUrl() {
        loader.style.display = 'block';
        resultCard.style.display = 'none';

        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            if (!tabs || tabs.length === 0 || !tabs[0].url || !tabs[0].url.startsWith('http')) {
                displayResult('error', 'Invalid URL', 'Cannot analyze local or browser-specific pages.');
                return;
            }
            
            const urlToCheck = tabs[0].url;
            urlDisplay.textContent = urlToCheck;

            fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: urlToCheck })
            })
            .then(response => {
                if (!response.ok) throw new Error(`API response error`);
                return response.json();
            })
            .then(data => {
                if (data.prediction === 'Phishing') {
                    displayResult('phishing', 'PHISHING', 'This URL has characteristics of a phishing site. Proceed with caution.');
                } else {
                    displayResult('legitimate', 'LEGITIMATE', 'This URL appears to be safe based on its structure.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                displayResult('error', 'API Offline', 'The backend server is not responding. Please ensure api.py is running.');
            });
        });
    }

    function displayResult(type, title, message) {
        loader.style.display = 'none';
        resultCard.className = type;
        resultText.textContent = title;
        resultMessage.textContent = message;

        resultIcon.className = ''; // Clear previous icon
        if (type === 'phishing') {
            resultIcon.classList.add('fas', 'fa-triangle-exclamation');
        } else if (type === 'legitimate') {
            resultIcon.classList.add('fas', 'fa-shield-halved');
        } else {
            resultIcon.classList.add('fas', 'fa-circle-question');
        }
        
        resultCard.style.display = 'block';
    }

    analyzeCurrentUrl();
});