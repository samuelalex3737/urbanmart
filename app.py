import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("transactions_1000.csv")
df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
df['date'] = pd.to_datetime(df['date'])
df['day_of_week'] = df['date'].dt.day_name()

st.title("UrbanMart Sales Dashboard")
st.write("Built by MAIB students using Python & Streamlit")

# Sidebar filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input("Select Date Range", [df['date'].min(), df['date'].max()])
store_filter = st.sidebar.multiselect("Select Store Location", df['store_location'].unique())
channel_filter = st.sidebar.selectbox("Select Channel", ["All"] + df['channel'].unique().tolist())
category_filter = st.sidebar.multiselect("Select Product Category", df['product_category'].unique())

# Apply filters
df_filtered = df.copy()
if len(date_range) == 2:
    df_filtered = df_filtered[(df_filtered['date'] >= pd.to_datetime(date_range[0])) &
                              (df_filtered['date'] <= pd.to_datetime(date_range[1]))]
if store_filter:
    df_filtered = df_filtered[df_filtered['store_location'].isin(store_filter)]
if channel_filter != "All":
    df_filtered = df_filtered[df_filtered['channel'] == channel_filter]
if category_filter:
    df_filtered = df_filtered[df_filtered['product_category'].isin(category_filter)]

# KPIs
st.subheader("Key Metrics")
st.metric("Total Revenue", round(df_filtered['line_revenue'].sum(), 2))
st.metric("Total Transactions", len(df_filtered['transaction_id'].unique()))
st.metric("Avg Revenue per Transaction", round(df_filtered['line_revenue'].mean(), 2))
st.metric("Unique Customers", df_filtered['customer_id'].nunique())

# Charts
st.subheader("Revenue by Category")
st.bar_chart(df_filtered.groupby('product_category')['line_revenue'].sum())

st.subheader("Revenue by Store")
st.bar_chart(df_filtered.groupby('store_location')['line_revenue'].sum())

st.subheader("Daily Revenue Trend")
st.line_chart(df_filtered.groupby('date')['line_revenue'].sum())

st.subheader("Top Products")
st.write(df_filtered.groupby('product_name')['line_revenue'].sum().sort_values(ascending=False).head(5))

st.subheader("Top Customers")
st.write(df_filtered.groupby('customer_id')['line_revenue'].sum().sort_values(ascending=False).head(5))

st.subheader("Sample Raw Data")

st.dataframe(df_filtered.head(20))
