import streamlit as st
import pandas as pd
import plotly.express as px
from utils.predict_expense import predict_next_expense
from ai.chatbot import finance_chatbot
from utils.financial_health import calculate_financial_health
from ai.finance_advisor import ai_finance_advisor
from utils.expense_classifier import predict_category
from utils.financial_report import generate_report

st.set_page_config(page_title="FinPilot AI", layout="wide")

# ---------------- THEME SWITCH ---------------- #

theme = st.sidebar.toggle("🌗 Dark / Light Mode")

if theme:
    bg = "#0e1117"
    text = "white"
else:
    bg = "white"
    text = "black"

# ---------------- CUSTOM CSS ---------------- #

st.markdown(f"""
<style>
body {{
background-color:{bg};
color:{text};
}}

.big-font {{
font-size:30px !important;
font-weight:700;
}}

.metric-card {{
background-color:#1f2c38;
padding:20px;
border-radius:10px;
text-align:center;
}}
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
"AI Financial Report"
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

# ---------------- SLIDER INPUTS ---------------- #

budget = st.sidebar.slider("💰 Monthly Budget", 0, 100000, 20000)

assets = st.sidebar.slider("🏦 Total Assets", 0, 2000000, 500000)

# ---------------- LOAD DATA ---------------- #

if uploaded_file is not None:
df = pd.read_csv(uploaded_file)
else:
df = pd.read_csv("data/expenses.csv")

df.columns = df.columns.str.strip().str.lower()

required_columns = ["date","amount","category"]

for col in required_columns:
if col not in df.columns:
st.error(f"Uploaded CSV must contain column: {col}")
st.stop()

df["date"] = pd.to_datetime(df["date"])

df["month"] = df["date"].dt.month_name()

# ---------------- DASHBOARD ---------------- #

if page == "Dashboard":

st.header("📊 Financial Overview")

col1,col2,col3,col4 = st.columns(4)

total_expense = df["amount"].sum()
predicted_expense = predict_next_expense()
score,advice = calculate_financial_health()
transactions = len(df)

col1.metric("💸 Total Expense",f"₹{total_expense}")
col2.metric("🔮 Predicted Expense",f"₹{predicted_expense}")
col3.metric("🧠 Financial Health",f"{score}/100")
col4.metric("📊 Transactions",transactions)

st.divider()

# ---------------- BUDGET TRACKER ---------------- #

st.subheader("💰 Budget Tracker")

spent = total_expense
remaining = budget - spent

b1,b2,b3 = st.columns(3)

b1.metric("Budget",f"₹{budget}")
b2.metric("Spent",f"₹{spent}")
b3.metric("Remaining",f"₹{remaining}")

st.progress(min(max(spent/budget,0),1))

st.divider()

# ---------------- NET WORTH ---------------- #

net_worth = assets - spent

st.subheader("📈 Net Worth Tracker")

st.metric("Your Net Worth",f"₹{net_worth}")

st.divider()

# ---------------- CHARTS ---------------- #

col4,col5 = st.columns(2)

with col4:
fig = px.pie(df,names="category",values="amount",title="Expense Distribution")
st.plotly_chart(fig,use_container_width=True)

with col5:
monthly_expense = df.groupby("month")["amount"].sum().reset_index()
fig2 = px.line(monthly_expense,x="month",y="amount",markers=True,title="Monthly Expense Trend")
st.plotly_chart(fig2,use_container_width=True)

st.divider()

# ---------------- AI INSIGHTS ---------------- #

st.subheader("🧠 AI Spending Insights")

top_category = df.groupby("category")["amount"].sum().idxmax()
avg_expense = df["amount"].mean()

st.success(f"Top spending category: **{top_category}**")
st.info(f"Average transaction expense: **₹{round(avg_expense,2)}**")
st.warning(advice)

st.divider()

# ---------------- TOP EXPENSES ---------------- #

st.subheader("💸 Top 5 Expenses")

top_exp = df.sort_values("amount",ascending=False).head(5)
st.dataframe(top_exp,use_container_width=True)

st.divider()

# ---------------- HEATMAP ---------------- #

st.subheader("🔥 Expense Heatmap")

heatmap_data = df.pivot_table(
values="amount",
index="category",
columns="month",
aggfunc="sum"
)

st.dataframe(heatmap_data)

st.divider()

# ---------------- DATASET ---------------- #

st.subheader("📊 Expense Dataset Preview")

st.dataframe(df.head(10),use_container_width=True)

# ---------------- EXPENSE INTELLIGENCE ---------------- #

elif page == "Expense Intelligence":

st.header("📊 Expense Breakdown")

category_expense = df.groupby("category")["amount"].sum()

st.bar_chart(category_expense)

# ---------------- PORTFOLIO ANALYZER ---------------- #

elif page == "Portfolio Analyzer":

import pages.portfolio_analyzer

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

st.subheader("Fill your details")

name = st.text_input("Your Name")
company = st.text_input("Company Name")
email = st.text_input("Email")

if st.button("Generate Report"):

pdf_path = generate_report()

st.success(f"Report generated for {name} ({company})")

with open(pdf_path,"rb") as file:

st.download_button(
label="📥 Download Financial Report PDF",
data=file,
file_name="FinPilot_Report.pdf",
mime="application/pdf"
)
