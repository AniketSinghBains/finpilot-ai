import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

from utils.predict_expense import predict_next_expense
from ai.chatbot import finance_chatbot
from utils.financial_health import calculate_financial_health
from ai.finance_advisor import ai_finance_advisor
from utils.expense_classifier import predict_category
from utils.financial_report import generate_report

st.set_page_config(page_title="FinPilot AI", layout="wide")

# ---------------- DARK MODE ---------------- #

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dark_toggle = st.sidebar.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = dark_toggle

plot_template = "plotly_dark" if st.session_state.dark_mode else "plotly"

if st.session_state.dark_mode:
    st.markdown("""
    <style>
    .stApp {
        background-color:#0E1117;
        color:white;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- TITLE ---------------- #

st.title("🚀 FinPilot AI — Personal Finance Intelligence")

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("📊 FinPilot Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Expense Intelligence",
        "Portfolio Analyzer",
        "AI Chatbot",
        "AI Finance Advisor",
        "Expense Classifier ML",
        "AI Financial Report",
        "Global Stock Explorer"
    ]
)

# ---------------- CSV UPLOAD ---------------- #

uploaded_file = st.sidebar.file_uploader("Upload Your Expense CSV", type=["csv"])

sample_data = pd.DataFrame({
    "date": ["2024-01-01", "2024-01-02"],
    "amount": [500, 1200],
    "category": ["Food", "Shopping"]
})

st.sidebar.download_button(
    "📥 Download Sample CSV",
    sample_data.to_csv(index=False),
    "sample_expenses.csv"
)

# ---------------- USER SETTINGS ---------------- #

budget = st.sidebar.slider("💰 Monthly Budget", 0, 100000, 20000)
assets = st.sidebar.slider("🏦 Total Assets", 0, 2000000, 500000)

# ---------------- LOAD DATA ---------------- #

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data/expenses.csv")

df.columns = df.columns.str.strip().str.lower()

df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.month_name()

# ---------------- DASHBOARD ---------------- #

if page == "Dashboard":

    st.header("📊 Financial Overview")

    col1, col2, col3, col4 = st.columns(4)

    total_expense = df["amount"].sum()
    predicted_expense = predict_next_expense()
    score, advice = calculate_financial_health()
    transactions = len(df)

    col1.metric("💸 Total Expense", f"₹{total_expense}")
    col2.metric("🔮 Predicted Expense", f"₹{predicted_expense}")
    col3.metric("🧠 Financial Health", f"{score}/100")
    col4.metric("📊 Transactions", transactions)

    st.divider()

    # Budget Tracker

    st.subheader("💰 Budget Tracker")

    spent = total_expense
    remaining = budget - spent

    b1, b2, b3 = st.columns(3)

    b1.metric("Budget", f"₹{budget}")
    b2.metric("Spent", f"₹{spent}")
    b3.metric("Remaining", f"₹{remaining}")

    st.progress(min(spent / budget, 1.0))

    st.divider()

    # Net Worth

    net_worth = assets - spent

    st.subheader("📈 Net Worth Tracker")
    st.metric("Your Net Worth", f"₹{net_worth}")

    st.divider()

    # Charts

    col4, col5 = st.columns(2)

    with col4:
        fig = px.pie(df, names="category", values="amount", title="Expense Distribution")
        fig.update_layout(template=plot_template)
        st.plotly_chart(fig, use_container_width=True)

    with col5:
        monthly_expense = df.groupby("month")["amount"].sum().reset_index()
        fig2 = px.line(monthly_expense, x="month", y="amount", markers=True)
        fig2.update_layout(template=plot_template)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # Financial Simulator

    st.subheader("⚙️ Financial Simulator")

    income = st.slider("Monthly Income", 10000, 500000, 50000)
    rent = st.slider("Rent / EMI", 0, 100000, 10000)
    food = st.slider("Food Expense", 0, 50000, 8000)
    shopping = st.slider("Shopping Expense", 0, 50000, 5000)
    investment = st.slider("Monthly Investment", 0, 100000, 10000)

    total_spending = rent + food + shopping
    savings = income - total_spending - investment

    st.metric("💰 Estimated Savings", f"₹{savings}")

    allocation_data = pd.DataFrame({
        "Category": ["Rent", "Food", "Shopping", "Investment", "Savings"],
        "Amount": [rent, food, shopping, investment, max(savings,0)]
    })

    fig_alloc = px.pie(allocation_data, names="Category", values="Amount", hole=0.4)
    fig_alloc.update_layout(template=plot_template)

    st.plotly_chart(fig_alloc, use_container_width=True)

# ---------------- STOCK MARKET ---------------- #

elif page == "Global Stock Explorer":

    st.header("🌍 Global Stock Market Explorer")

    ticker = st.text_input("Enter Stock Ticker (AAPL, TSLA, INFY, RELIANCE.NS)")

    if ticker:

        stock = yf.Ticker(ticker)

        data = stock.history(period="1y")

        st.subheader(f"{ticker} Stock Price")

        fig = px.line(data, x=data.index, y="Close", title=f"{ticker} Price Chart")

        fig.update_layout(template=plot_template)

        st.plotly_chart(fig, use_container_width=True)

        latest_price = data["Close"].iloc[-1]

        st.metric("Latest Price", f"${round(latest_price,2)}")

        # Investment Simulator

        st.subheader("💰 Investment Simulator")

        amount = st.number_input("Enter Investment Amount", min_value=100)

        if amount:

            shares = amount / latest_price

            st.success(f"You can buy approx **{round(shares,2)} shares** of {ticker}")

# ---------------- CHATBOT ---------------- #

elif page == "AI Chatbot":

    st.header("🤖 FinPilot AI Assistant")

    user_question = st.text_input("Ask a finance question")

    if user_question:
        answer = finance_chatbot(user_question)
        st.success(answer)

# ---------------- FINANCE ADVISOR ---------------- #

elif page == "AI Finance Advisor":

    st.header("🧠 AI Personal Finance Advisor")

    question = st.text_input("Ask your finance question")

    if question:
        advice = ai_finance_advisor(question)
        st.success(advice)

# ---------------- EXPENSE CLASSIFIER ---------------- #

elif page == "Expense Classifier ML":

    st.header("🤖 Expense Category Predictor")

    description = st.text_input("Expense Description")

    if description:
        category = predict_category(description)
        st.success(f"Predicted Category: {category}")

# ---------------- REPORT GENERATOR ---------------- #

elif page == "AI Financial Report":

    st.header("📊 AI Financial Report Generator")

    name = st.text_input("Your Name")
    company = st.text_input("Company Name")
    email = st.text_input("Email")

    if st.button("Generate Report"):

        pdf_path = generate_report(name, company, email)

        st.success(f"Report generated for {name}")

        with open(pdf_path, "rb") as file:

            st.download_button(
                label="📥 Download Financial Report PDF",
                data=file,
                file_name="FinPilot_Report.pdf",
                mime="application/pdf"
            )
