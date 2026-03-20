import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report():

    df = pd.read_csv("data/expenses.csv")

    total_spent = df["amount"].sum()
    avg_expense = df["amount"].mean()
    top_category = df.groupby("category")["amount"].sum().idxmax()

    report_text = f"""
    Monthly Financial Report

    Total Spending: ₹{total_spent}

    Average Expense: ₹{round(avg_expense,2)}

    Highest Spending Category: {top_category}

    Savings Suggestion:
    Try reducing spending in {top_category}.

    Investment Advice:
    Consider investing in index funds, ETFs and diversified portfolios.
    """

    pdf_path = "financial_report.pdf"

    styles = getSampleStyleSheet()

    elements = []

    for line in report_text.split("\n"):
        elements.append(Paragraph(line, styles["Normal"]))
        elements.append(Spacer(1,10))

    pdf = SimpleDocTemplate(pdf_path)

    pdf.build(elements)

    return pdf_path
