import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

def train_model():
    df = pd.read_excel("data/urban_growth_dataset.xlsx")

    df['growth_velocity'] = (
        df['population'] * 0.3 +
        df['price_index'] * 0.3 +
        df['infra_score'] * 0.2 +
        df['employment_rate'] * 0.2
    )

    X = df[['population', 'price_index', 'infra_score', 'employment_rate']]
    y = df['growth_velocity']

    model = LinearRegression()
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/model.pkl")

    print("Model saved successfully!")

def load_model():
    return joblib.load("models/model.pkl")

if __name__ == "__main__":
    train_model()