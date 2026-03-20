import pandas as pd
from sklearn.linear_model import LinearRegression

def predict_next_expense():

    df = pd.read_csv("data/expenses.csv")

    df["date"] = pd.to_datetime(df["date"])

    df["day"] = df["date"].dt.day

    X = df[["day"]]
    y = df["amount"]

    model = LinearRegression()
    model.fit(X, y)

    next_day = [[31]]

    prediction = model.predict(next_day)

    return round(prediction[0], 2)