import os
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

def train_model():
    df = pd.read_csv("data/urban_growth_dataset.csv")

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

    return model


def load_model():
    model_path = "models/model.pkl"

    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        return train_model()