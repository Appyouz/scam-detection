# Catch the Phish! 🎣(Scam Detection Program)

An educational and practical web application for detecting phishing attempts in email content. This project serves as a full-stack example, demonstrating a Django backend that integrates a pre-trained machine learning model and communicates with a modern JavaScript frontend using asynchronous requests.

This application is built as a portfolio piece to showcase skills in web development, API integration, and machine learning model deployment.

## ✨ Features

- **Frontend**: A user-friendly, single-page interface for pasting email content.
- **Backend**: A RESTful API built with Django to handle requests.
- **Asynchronous Communication**: Uses the Fetch API to send data to the backend without reloading the page.
- **Machine Learning Integration**: Loads a pre-trained `scikit-learn` model to make real-time predictions.
- **URL Feature Extraction**: Contains custom logic to parse a URL and extract over 50 numerical features for the model.

## 🚀 Technologies

* **Backend**: Python, Django
* **Frontend**: HTML5, CSS3, JavaScript (ES6+)
* **Machine Learning**: `joblib`, `scikit-learn`, `pandas`
* **Environment**: `pip`, Virtual Environments
* **Version Control**: Git

## 🛠️ Prerequisites

Before you can run the project, ensure you have the following installed:

* **Python**: Version 3.8 or higher.
* **pip**: Python's package installer.
* **Git**: For cloning the repository.

## ⚙️ Installation and Setup

Follow these steps to get the project up and running on your local machine.

1.  **Clone the Repository**

    ```bash
    git clone git@github.com:Appyouz/scam-detection.git
    cd scam-detection
    ```

2.  **Create and Activate a Virtual Environment**

    It's a best practice to use a virtual environment to manage project dependencies.

    ```bash
    python -m venv .venv
    # On Linux/macOS
    source .venv/bin/activate
    # On Windows
    .venv\Scripts\activate
    ```

3.  **Install Dependencies**

    Install all the required Python packages using pip.

    ```bash
    pip install django
    pip install joblib
    pip install scikit-learn
    pip install pandas
    ```
    Or
    ```bash
    pip install -r requirements.txt
    ```

4.  **Place the Pre-trained Model**

    The machine learning model (`scam_detector_model.pkl`) is  included in the repository. You can obtain your own model file  and place it in the following directory:

    ```
    ml_model/data/
    ```

5.  **Run the Django Server**

    Start the development server.

    ```bash
    python manage.py runserver
    ```

    The application will be accessible at `http://127.0.0.1:8000/`.

## 🖥️ Usage

1.  Navigate to `http://127.0.0.1:8000/` in your web browser.
2.  Paste any email or URL content into the textarea.
3.  Click the “Analyze” button.
4.  The application will display “Safe” or “Malicious”  based on the analysis.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.
