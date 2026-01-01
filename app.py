import pandas as pd
from flask import Flask, jsonify, request
import kagglehub
from kagglehub import KaggleDatasetAdapter
import json
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

app = Flask(__name__)
CORS(app)

# ---------------- LOAD DATASET ----------------
try:
    print("Loading dataset from Kaggle Hub...")

    df = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "asaniczka/tmdb-movies-dataset-2023-930k-movies",
        path="TMDB_movie_dataset_v11.csv"
    )

    print("Dataset loaded successfully")

    # ---------- DATA CLEANING ----------
    df['genres'] = df['genres'].fillna('[]')
    df['keywords'] = df['keywords'].fillna('[]')
    df['title'] = df['title'].fillna('')
    df['budget'] = df['budget'].fillna(0)
    df['revenue'] = df['revenue'].fillna(0)
    df['popularity'] = df['popularity'].fillna(0)
    df['vote_average'] = df['vote_average'].fillna(0)
    df['vote_count'] = df['vote_count'].fillna(0)

    def extract_names(json_str):
        try:
            items = json.loads(json_str)
            return ", ".join(item.get("name", "") for item in items)
        except Exception:
            return ""

    df['genre_names'] = df['genres'].apply(extract_names)
    df['keyword_names'] = df['keywords'].apply(extract_names)

    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

    print("Data preprocessing complete")

except Exception as e:
    print("FATAL ERROR:", e)
    df = pd.DataFrame()

# ---------------- ML MODEL ----------------
try:
    print("Training ML model...")

    if not df.empty:
        features = ['budget', 'popularity', 'vote_average', 'vote_count']
        X = df[features]
        y = df['revenue']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = LinearRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)

        print(f"Model trained successfully | MAE: {mae:.2f}")
    else:
        model = None

except Exception as e:
    print("Model training failed:", e)
    model = None

# ---------------- API ROUTES ----------------
@app.route("/api/movies", methods=["GET"])
def get_movies():
    if df.empty:
        return jsonify({"error": "Dataset not available"}), 500

    movies = df.sort_values(by="popularity", ascending=False).head(50)

    return jsonify(movies.to_dict(orient="records"))


@app.route("/api/search", methods=["GET"])
def search_movies():
    if df.empty:
        return jsonify({"error": "Dataset not available"}), 500

    query = request.args.get("q", "").lower()

    if not query:
        return jsonify({"error": "Search query missing"}), 400

    results = df[
        df['title'].str.lower().str.contains(query, na=False)
    ].head(50)

    return jsonify(results.to_dict(orient="records"))


@app.route("/api/predict", methods=["POST"])
def predict_revenue():
    if model is None:
        return jsonify({"error": "Model not available"}), 500

    data = request.json

    try:
        features = [
            data.get("budget", 0),
            data.get("popularity", 0),
            data.get("vote_average", 0),
            data.get("vote_count", 0)
        ]

        prediction = model.predict([features])[0]
        return jsonify({"predicted_revenue": round(float(prediction), 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)
