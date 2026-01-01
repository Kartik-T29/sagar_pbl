# Movie Success Prediction

This project is a web application that predicts the success of movies using a machine learning model. It features a Python Flask backend that serves movie data from a Kaggle dataset and a JavaScript frontend to display the information and interact with the user.

## Features

*   **Dynamic Movie Data:** Loads the "TMDB 5000 Movie Dataset" directly from Kaggle Hub.
*   **Search Functionality:** Search for movies by title, genre, or keywords.
*   **Popular Movies:** Displays a list of the most popular movies on page load.
*   **Movie Details:** View detailed information for each movie in a modal pop-up.
*   **ML-Powered Predictions:** Input movie details (budget, genre, etc.) to get a predicted revenue, ROI, and success score from a trained linear regression model.

## How to Run the Application

This project consists of a Python backend and a JavaScript frontend. You need to run the backend server first before you can view the application in your browser.

### Prerequisites

*   Python 3.6+
*   `pip` (Python package installer)
*   A Kaggle account and an API token (`kaggle.json`)

### Step 1: Install Dependencies

Open a terminal or command prompt in the project's root directory and install the required Python libraries by running:

```bash
pip install -r requirements.txt
```

### Step 2: Set Up Kaggle API Credentials

In order to download the movie dataset, the backend needs access to your Kaggle API credentials.

1.  **Download your API Token:** Go to your Kaggle account page (e.g., `https://www.kaggle.com/YourUsername/account`) and click on **Create New API Token**. This will download a `kaggle.json` file.
    *   If the file does not download automatically, you can manually create a file named `kaggle.json` and paste the credentials displayed on the screen.

2.  **Place the API Token:**
    *   **For Linux/macOS:** Create a folder named `.kaggle` in your home directory (`~/.kaggle`) and place the `kaggle.json` file inside it.
    *   **For Windows:** Create a folder named `.kaggle` in your user profile directory (`C:\Users\<Your-Username>\.kaggle`) and place the `kaggle.json` file inside it.

### Step 3: Run the Backend Server

Once the dependencies are installed and your Kaggle API key is set up, you can start the backend server. Run the following command in your terminal from the project's root directory:

```bash
python app.py
```

If successful, you will see messages in the terminal indicating the server is running on `http://127.0.0.1:5001`. The first time you run this, it will also download the dataset from Kaggle, which may take a moment.

### Step 4: View the Application

Open the `index.html` file in your favorite web browser.

The page should now load correctly, displaying a grid of popular movies. You can use the search bar to find specific movies, and use the prediction form to get success estimates for new movie ideas.
