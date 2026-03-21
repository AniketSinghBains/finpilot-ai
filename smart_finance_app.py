import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
import pydeck as pdk

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

# ---------------- TITLE ---------------- #

st.title("🚀 FinPilot AI — Personal Finance Intelligence")

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("📊 FinPilot Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Expense Intelligence",
        "📊 Dataset Explorer",
        "Portfolio Analyzer",
        "AI Chatbot",
        "AI Finance Advisor",
        "Expense Classifier ML",
        "AI Financial Report",
        "🌍 Global Stock Explorer"
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

required_columns = ["date", "amount", "category"]

for col in required_columns:
    if col not in df.columns:
        st.error(f"Uploaded CSV must contain column: {col}")
        st.stop()

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

    col4, col5 = st.columns(2)

    with col4:
        fig = px.pie(df, names="category", values="amount")
        fig.update_layout(template=plot_template)
        st.plotly_chart(fig, use_container_width=True)

    with col5:
        monthly_expense = df.groupby("month")["amount"].sum().reset_index()
        fig2 = px.line(monthly_expense, x="month", y="amount", markers=True)
        fig2.update_layout(template=plot_template)
        st.plotly_chart(fig2, use_container_width=True)

# ---------------- DATASET EXPLORER ---------------- #

elif page == "📊 Dataset Explorer":

    st.header("📊 Expense Dataset Explorer")

    col1, col2 = st.columns(2)

    with col1:
        search = st.text_input("🔍 Search Category")

    with col2:
        sort_order = st.selectbox(
            "Sort By Date",
            ["Newest First", "Oldest First"]
        )

    filtered_df = df

    if search:
        filtered_df = filtered_df[
            filtered_df["category"].str.contains(search, case=False)
        ]

    if sort_order == "Newest First":
        filtered_df = filtered_df.sort_values("date", ascending=False)
    else:
        filtered_df = filtered_df.sort_values("date", ascending=True)

    st.dataframe(filtered_df, use_container_width=True)

    st.success(f"Total Records: {len(filtered_df)}")

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Filtered Dataset",
        csv,
        "filtered_expenses.csv",
        "text/csv"
    )

# ---------------- GLOBAL STOCK EXPLORER ---------------- #

elif page == "🌍 Global Stock Explorer":

    st.header("🌍 Global Stock Market Explorer")

    ticker = st.text_input("Enter Stock Ticker (AAPL, TSLA, INFY, RELIANCE.NS)")

    if ticker:

        data = yf.download(ticker, period="6mo")

        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"]
        )])

        fig.update_layout(title=f"{ticker} Trading Chart", template=plot_template)

        st.plotly_chart(fig, use_container_width=True)

        latest_price = data["Close"].iloc[-1]

        st.metric("Latest Price", f"${round(latest_price,2)}")

        data["SMA20"] = data["Close"].rolling(20).mean()
        data["SMA50"] = data["Close"].rolling(50).mean()

        short = data["SMA20"].iloc[-1]
        long = data["SMA50"].iloc[-1]

        st.subheader("🤖 AI Trading Signal")

        if short > long:
            st.success("📈 BUY Signal")
        else:
            st.error("📉 SELL Signal")

        st.subheader("💰 Investment Simulator")

        amount = st.number_input("Investment Amount", min_value=100)

        if amount:
            shares = amount / latest_price
            st.success(f"You can buy approx **{round(shares,2)} shares**")

    st.subheader("🌍 Global Market Map")

    map_data = pd.DataFrame({
        "company": ["Apple", "Tesla", "Infosys", "Toyota"],
        "lat": [37.3349, 30.2672, 12.9716, 35.6762],
        "lon": [-122.0090, -97.7431, 77.5946, 139.6503]
    })

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_data,
        get_position='[lon, lat]',
        get_radius=50000,
        get_fill_color=[200, 30, 0, 160],
    )

    view_state = pdk.ViewState(
        latitude=20,
        longitude=0,
        zoom=1,
    )

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state
    ))

# ---------------- OTHER PAGES ---------------- #

elif page == "Expense Intelligence":

    st.header("📊 Expense Breakdown")
    category_expense = df.groupby("category")["amount"].sum()
    st.bar_chart(category_expense)

elif page == "Portfolio Analyzer":
    import pages.portfolio_analyzer

elif page == "AI Chatbot":

    st.header("🤖 FinPilot AI Assistant")

    user_question = st.text_input("Ask a finance question")

    if user_question:
        answer = finance_chatbot(user_question)
        st.success(answer)

elif page == "AI Finance Advisor":

    st.header("🧠 AI Personal Finance Advisor")

    question = st.text_input("Ask your finance question")

    if question:
        advice = ai_finance_advisor(question)
        st.success(advice)

elif page == "Expense Classifier ML":

    st.header("🤖 Expense Category Predictor")

    description = st.text_input("Expense Description")

    if description:
        category = predict_category(description)
        st.success(f"Predicted Category: {category}")

elif page == "AI Financial Report":

    st.header("📊 AI Financial Report Generator")

    name = st.text_input("Your Name")
    company = st.text_input("Company Name")
    email = st.text_input("Email")

    if st.button("Generate Report"):

        pdf_path = generate_report(name, company, email)

        st.success(f"Report generated for {name} ({company})")

        with open(pdf_path, "rb") as file:

            st.download_button(
                label="📥 Download Financial Report PDF",
                data=file,
                file_name="FinPilot_Report.pdf",
                mime="application/pdf"
            )
