import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit page setup
st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")
st.title("📊 Superstore Sales Analysis Dashboard")

# Load dataset
df = pd.read_csv("Superstore.csv", encoding='ISO-8859-1')

# Sidebar filters
st.sidebar.header("🔍 Filters")
region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
category = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())

# Apply filters
df_filtered = df[df['Region'].isin(region) & df['Category'].isin(category)]

# Display KPIs
st.markdown("### 📌 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df_filtered['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${df_filtered['Profit'].sum():,.2f}")
col3.metric("Total Orders", df_filtered['Order ID'].nunique())

st.markdown("---")

# Sales by Category
st.subheader("📦 Sales by Category")
fig1, ax1 = plt.subplots()
sns.barplot(data=df_filtered, x='Category', y='Sales', estimator=sum, ci=None, ax=ax1)
ax1.set_title("Sales by Category")
st.pyplot(fig1)

# Profit by City (Top 10 Positive and Negative)
st.subheader("🏙️ Top Cities by Profit")
city_profit = df_filtered.groupby('City')['Profit'].sum().sort_values(ascending=False)
fig2, ax2 = plt.subplots(1, 2, figsize=(16, 5))
city_profit.head(10).plot(kind='barh', ax=ax2[0], color='green')
ax2[0].set_title("Top 10 Profitable Cities")
city_profit.tail(10).plot(kind='barh', ax=ax2[1], color='red')
ax2[1].set_title("Top 10 Loss-Making Cities")
st.pyplot(fig2)

# Discount vs Profit
st.subheader("💸 Discount vs Profit")
fig3, ax3 = plt.subplots()
sns.scatterplot(data=df_filtered, x='Discount', y='Profit', hue='Category', ax=ax3)
ax3.set_title("Impact of Discount on Profit")
st.pyplot(fig3)

# Region-wise Sales
st.subheader("🧭 Sales by Region")
region_sales = df_filtered.groupby('Region')['Sales'].sum()
fig4, ax4 = plt.subplots()
region_sales.plot(kind='pie', autopct='%1.1f%%', ax=ax4)
ax4.set_ylabel('')
ax4.set_title("Sales Distribution by Region")
st.pyplot(fig4)

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
