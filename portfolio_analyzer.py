import streamlit as st
import pandas as pd
import plotly.express as px

st.header("📈 Investment Portfolio Analyzer")

df = pd.read_csv("data/portfolio.csv")

st.subheader("Portfolio Data")

st.dataframe(df)

# Total Investment
total_investment = df["investment"].sum()

# Current Value
total_current = df["current_value"].sum()

# Profit / Loss
profit = total_current - total_investment

st.metric("Total Investment", f"₹{total_investment}")
st.metric("Current Value", f"₹{total_current}")
st.metric("Profit / Loss", f"₹{profit}")

# Asset Distribution
fig = px.pie(
    df,
    names="asset",
    values="current_value",
    title="Portfolio Distribution"
)

st.plotly_chart(fig)

# Best Asset
best_asset = df.loc[df["current_value"].idxmax()]["asset"]

st.success(f"Best performing asset: {best_asset}")