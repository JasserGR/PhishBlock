# PhishBlock: A Phishing URL Detection Browser Extension

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

-   **Automatic Real-Time Detection:** Automatically analyzes the current browser URL as soon as the extension is opened.
-   **Robust Model:** Uses a Random Forest classifier trained on 11 reliably extractable URL features, achieving ~75% accuracy on a holdout test set.
-   **Modern UI:** A clean, modern user interface provides instant, color-coded feedback on the safety of a URL.
-   **Full End-to-End System:** A complete application with a separate frontend (browser extension) and backend (Flask API).
-   **Demonstrates Critical Debugging:** The project successfully overcame a real-world "training-serving skew" problem by re-engineering the model and features to create a reliable prediction pipeline.

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
    # Create and activate a virtual environment
    python -m venv venv
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
    -   The popup will open and **automatically** display the prediction for the current URL.
