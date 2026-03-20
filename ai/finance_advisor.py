import pandas as pd

def ai_finance_advisor(question):

    question = question.lower()

    df = pd.read_csv("data/expenses.csv")

    total_spent = df["amount"].sum()
    avg_spent = df["amount"].mean()

    top_category = df.groupby("category")["amount"].sum().idxmax()

    # -------- Advice Logic -------- #

    if "save" in question or "saving" in question:
        return f"You spent ₹{total_spent}. Try reducing spending in {top_category} to increase savings."

    elif "investment" in question:
        return "Consider diversifying your investments into stocks, index funds, and bonds."

    elif "expense" in question:
        return f"Your average expense is ₹{round(avg_spent,2)}. Monitor high spending categories."

    elif "budget" in question:
        return "Use the 50/30/20 rule: 50% needs, 30% wants, 20% savings."

    else:
        return "Focus on reducing unnecessary expenses and increasing savings rate."
