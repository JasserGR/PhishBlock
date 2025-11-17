# 🎣 PhishBlock: A Phishing URL Detection Browser Extension

PhishBlock is a complete machine learning project that uses a Random Forest model to detect phishing websites in real-time. The project includes a Python backend API built with Flask and a functional browser extension for live URL analysis.

---

## 🚀 Tech Stack

-   **Python:** Core language for the backend and model training.
-   **Machine Learning:** Scikit-learn, Pandas, Joblib.
-   **Backend API:** Flask.
-   **Browser Extension:** HTML, CSS, JavaScript (Manifest V3).
-   **Data Source:** Phishing Website Features Dataset from Kaggle.

---

## ✨ Features

-   **Real-Time Detection:** Analyze the current browser URL with a single click.
-   **Robust Model:** Uses a Random Forest classifier trained on 11 reliably extractable URL features, achieving ~75% accuracy on a holdout test set.
-   **Full End-to-End System:** A complete application with a separate frontend (browser extension) and backend (Flask API).
-   **Demonstrates Critical Debugging:** The project successfully overcame a real-world "training-serving skew" problem by reverse-engineering opaque feature logic to create a reliable prediction pipeline.

---

## 📦 How to Run

### Prerequisites
-   Python 3.8+
-   Google Chrome

### Instructions

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/JasserGR/PhishBlock.git
    cd PhishBlock
    ```

2.  **Set Up and Run the Backend:**
    ```bash
    # Create a virtual environment
    python -m venv venv

    # Activate it (Windows)
    .\venv\Scripts\activate

    # Install required libraries
    pip install -r requirements.txt

    # Run the Flask API server
    python api.py
    ```
    *Leave this terminal running.*

3.  **Load the Browser Extension:**
    -   Open Google Chrome and navigate to `chrome://extensions`.
    -   Enable "Developer mode" in the top right corner.
    -   Click "Load unpacked".
    -   Select the `extension` folder from the project directory.

4.  **Test:**
    -   Navigate to any website.
    -   Click the PhishBlock icon in your toolbar.
    -   Click "Check Current URL" to see the prediction.