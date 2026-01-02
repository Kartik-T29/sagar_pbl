from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

from data_loader import load_dataset
from model import train_model

app = Flask(__name__)
CORS(app)

# ---------- LOAD DATA ONCE ----------
df = load_dataset()
model = train_model(df)

# ---------- ROUTES ----------

@app.route("/api/movies")
def popular_movies():
    movies = df.sort_values("popularity", ascending=False).head(30)
    return jsonify(movies.to_dict(orient="records"))


@app.route("/api/search")
def search():
    q = request.args.get("q", "").lower()
    results = df[df["title"].str.lower().str.contains(q, na=False)].head(30)
    return jsonify(results.to_dict(orient="records"))


@app.route("/api/upcoming")
def upcoming():
    upcoming = df[df["release_date"] > pd.Timestamp.today()]
    upcoming = upcoming.sort_values("release_date").head(20)
    return jsonify(upcoming.to_dict(orient="records"))


@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.json

    budget = float(data.get("budget", 0))
    popularity = float(data.get("tmdb_popularity", 0))
    vote_average = 6.5
    vote_count = 500

    revenue = model.predict([[budget, popularity, vote_average, vote_count]])[0]
    roi = round(revenue / budget, 2) if budget else 0
    score = min(100, int(roi * 20))

    return jsonify({
        "revenue": round(revenue, 2),
        "roi": roi,
        "score": score
    })

@app.route("/")
def home():
    return jsonify({
        "status": "API is running",
        "routes": [
            "/api/movies",
            "/api/search?q=movie_name",
            "/api/upcoming",
            "/api/predict (POST)"
        ]
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)
