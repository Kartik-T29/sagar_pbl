from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def train_model(df):
    features = ["budget", "popularity", "vote_average", "vote_count"]
    X = df[features]
    y = df["revenue"]

    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    print("🤖 ML Model trained")
    return model
