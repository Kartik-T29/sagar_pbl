import os
import json
import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter

DATA_PATH = "movies_cleaned.csv"

def extract_names(json_str):
    try:
        items = json.loads(json_str)
        return ", ".join([i.get("name", "") for i in items])
    except:
        return ""

def load_dataset():
    # 👉 If cleaned dataset exists, load it
    if os.path.exists(DATA_PATH):
        print("✅ Loading cached dataset...")
        return pd.read_csv(DATA_PATH)

    print("⬇️ Downloading dataset from Kaggle (ONE TIME)...")

    df = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "asaniczka/tmdb-movies-dataset-2023-930k-movies",
        path="TMDB_movie_dataset_v11.csv"
    )

    print("🧹 Cleaning dataset...")

    df = df[
        (df["budget"] > 0) &
        (df["revenue"] > 0) &
        (df["vote_count"] > 50)
    ]

    df["genres"] = df["genres"].fillna("[]")
    df["genre_names"] = df["genres"].apply(extract_names)

    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["popularity"] = df["popularity"].fillna(0)
    df["vote_average"] = df["vote_average"].fillna(0)

    keep_cols = [
        "title",
        "budget",
        "revenue",
        "popularity",
        "vote_average",
        "vote_count",
        "genre_names",
        "release_date",
        "overview",
        "poster_path"
    ]

    df = df[keep_cols]

    df.to_csv(DATA_PATH, index=False)
    print("💾 Cleaned dataset saved locally")

    return df
