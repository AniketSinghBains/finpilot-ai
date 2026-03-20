import pandas as pd

def calculate_financial_health():

    df = pd.read_csv("data/expenses.csv")

    total_expense = df["amount"].sum()

    avg_expense = df["amount"].mean()

    top_category = df.groupby("category")["amount"].sum().idxmax()

    score = 100

    if total_expense > 8000:
        score -= 20

    if avg_expense > 1000:
        score -= 15

    if top_category == "Shopping":
        score -= 10

    advice = "Your finances look healthy."

    if score < 70:
        advice = "Try reducing non-essential spending like Shopping."

    return score, advice