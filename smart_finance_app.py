import streamlit as st
import pandas as pd
import plotly.express as px
from utils.predict_expense import predict_next_expense
from ai.chatbot import finance_chatbot
from utils.financial_health import calculate_financial_health
from ai.finance_advisor import ai_finance_advisor
from utils.expense_classifier import predict_category
from utils.financial_report import generate_report   # STEP 4: Import report generator

st.set_page_config(page_title="FinPilot AI", layout="wide")

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>
.big-font {
    font-size:28px !important;
    font-weight:700;
}

.metric-card {
    background-color:#1f2c38;
    padding:20px;
    border-radius:10px;
    text-align:center;
}

.sidebar .sidebar-content {
    background-color:#0f172a;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #

st.markdown('<p class="big-font">🚀 FinPilot AI — Personal Finance Intelligence</p>', unsafe_allow_html=True)

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
        "AI Financial Report"   # STEP 5: New Page Added
    ]
)

# ---------------- LOAD DATA ---------------- #

df = pd.read_csv("data/expenses.csv")
df.columns = df.columns.str.strip()

df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.month_name()

# ---------------- DASHBOARD ---------------- #

if page == "Dashboard":

    st.header("📊 Financial Overview")

    col1, col2, col3 = st.columns(3)

    total_expense = df["amount"].sum()
    predicted_expense = predict_next_expense()
    score, advice = calculate_financial_health()

    with col1:
        st.metric("💸 Total Expense", f"₹{total_expense}")

    with col2:
        st.metric("🔮 Predicted Next Expense", f"₹{predicted_expense}")

    with col3:
        st.metric("🧠 Financial Health", f"{score}/100")

    st.divider()

    col4, col5 = st.columns(2)

    with col4:

        fig = px.pie(
            df,
            names="category",
            values="amount",
            title="Expense Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col5:

        monthly_expense = df.groupby("month")["amount"].sum().reset_index()

        fig2 = px.line(
            monthly_expense,
            x="month",
            y="amount",
            markers=True,
            title="Monthly Expense Trend"
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("📊 Financial Insights")

    top_category = df.groupby("category")["amount"].sum().idxmax()
    avg_expense = df["amount"].mean()

    st.info(f"Highest spending category: **{top_category}**")
    st.info(f"Average transaction expense: **₹{round(avg_expense,2)}**")

    st.warning(advice)

    # ---------------- DATASET PREVIEW ---------------- #

    st.divider()

    st.subheader("📊 Expense Dataset Preview")

    st.dataframe(df.head(10), use_container_width=True)


# ---------------- EXPENSE INTELLIGENCE ---------------- #

elif page == "Expense Intelligence":

    st.header("📊 Expense Breakdown")

    category_expense = df.groupby("category")["amount"].sum()

    st.bar_chart(category_expense)


# ---------------- PORTFOLIO ANALYZER ---------------- #

elif page == "Portfolio Analyzer":

    import pages.portfolio_analyzer


# ---------------- AI CHATBOT ---------------- #

elif page == "AI Chatbot":

    st.header("🤖 FinPilot AI Assistant")

    st.write("Ask questions about your spending.")

    user_question = st.text_input("Ask a finance question")

    if user_question:

        answer = finance_chatbot(user_question)

        st.success(answer)


# ---------------- AI FINANCE ADVISOR ---------------- #

elif page == "AI Finance Advisor":

    st.header("🧠 AI Personal Finance Advisor")

    st.write("Ask anything about saving, budgeting or investments.")

    question = st.text_input("Ask your finance question")

    if question:

        advice = ai_finance_advisor(question)

        st.success(advice)


# ---------------- EXPENSE CLASSIFIER ML ---------------- #

elif page == "Expense Classifier ML":

    st.header("🤖 Expense Category Predictor")

    st.write("Enter expense description to predict category")

    description = st.text_input("Expense Description")

    if description:

        category = predict_category(description)

        st.success(f"Predicted Category: {category}")


# ---------------- AI FINANCIAL REPORT ---------------- #

elif page == "AI Financial Report":   # STEP 6: Report Generator Page

    st.header("📊 AI Financial Report Generator")

    st.write("Generate your monthly financial report.")

    if st.button("Generate Report"):

        pdf_path = generate_report()

        with open(pdf_path, "rb") as file:

            st.download_button(
                label="📥 Download Financial Report PDF",
                data=file,
                file_name="FinPilot_Report.pdf",
                mime="application/pdf"
            )