import pandas as pd

def finance_chatbot(question):

    df = pd.read_csv("data/expenses.csv")

    question = question.lower()

    if "highest" in question or "most" in question:

        top_category = df.groupby("category")["amount"].sum().idxmax()
        return f"You spend the most on {top_category}."

    elif "total" in question:

        total = df["amount"].sum()
        return f"Your total spending is ₹{total}."

    elif "average" in question:

        avg = df["amount"].mean()
        return f"Your average expense is ₹{round(avg,2)}."

    elif "food" in question:

        food = df[df["category"]=="Food"]["amount"].sum()
        return f"You spent ₹{food} on Food."

    else:

        return "I can help analyze your spending. Try asking about total spending, highest category, or averages."