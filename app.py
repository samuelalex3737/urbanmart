import streamlit as st
import pandas as pd
import altair as alt

# Load data
df = pd.read_csv("transactions_1000.csv")
df['date'] = pd.to_datetime(df['date'], format="%d-%m-%Y")
df['quarter'] = df['date'].dt.to_period("Q").astype(str)
df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']

# --- Dashboard Styling ---
st.set_page_config(page_title="UrbanMart Dashboard", layout="wide")

PRIMARY = "#4CAF50"
SECONDARY = "#2196F3"
ACCENT = "#FF9800"

st.markdown(
    f"""
    <style>
        .metric-box {{
            background-color: #f7f7f7;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid {PRIMARY};
        }}
        .section-title {{
            font-size: 22px;
            font-weight: 600;
            color: {PRIMARY};
            margin-top: 30px;
        }}
        .highlight {{
            background-color: #e8f5e9;
            padding: 15px;
            border-radius: 8px;
            border-left: 5px solid {ACCENT};
            margin-bottom: 15px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Title ---
st.title("UrbanMart Sales Intelligence Dashboard")
st.write("A compact, executive-ready analytics dashboard.")

# --- KPIs ---
st.markdown("<div class='section-title'>Key Performance Indicators</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.metric("Total Revenue", round(df['line_revenue'].sum(), 2))
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.metric("Total Transactions", df['transaction_id'].nunique())
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.metric("Avg Revenue per Transaction", round(df['line_revenue'].mean(), 2))
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.metric("Unique Customers", df['customer_id'].nunique())
    st.markdown("</div>", unsafe_allow_html=True)

# --- QUARTERLY REVENUE ---
st.markdown("<div class='section-title'>Quarterly Revenue Analysis</div>", unsafe_allow_html=True)

quarter_filter = st.multiselect("Select Quarter", df['quarter'].unique())

df_q = df.copy()
if quarter_filter:
    df_q = df_q[df_q['quarter'].isin(quarter_filter)]

quarter_data = df_q.groupby("quarter")["line_revenue"].sum().reset_index()

if len(quarter_filter) == 1:
    q = quarter_filter[0]
    rev = quarter_data.loc[quarter_data['quarter'] == q, 'line_revenue'].values[0]
    st.markdown(f"<div class='highlight'>Revenue for <b>{q}</b> is <b>{rev:.2f}</b>.</div>", unsafe_allow_html=True)
else:
    chart = (
        alt.Chart(quarter_data)
        .mark_bar(color=PRIMARY)
        .encode(
            x="quarter:N",
            y="line_revenue:Q",
            tooltip=["quarter", "line_revenue"]
        )
    )
    st.altair_chart(chart, use_container_width=True)

# --- CATEGORY REVENUE ---
st.markdown("<div class='section-title'>Revenue by Category</div>", unsafe_allow_html=True)

category_filter = st.multiselect("Filter Category", df['product_category'].unique())

df_cat = df.copy()
if category_filter:
    df_cat = df_cat[df_cat['product_category'].isin(category_filter)]

cat_data = df_cat.groupby("product_category")["line_revenue"].sum().reset_index()

if len(category_filter) == 1:
    cat = category_filter[0]
    rev = cat_data.loc[cat_data['product_category'] == cat, 'line_revenue'].values[0]
    st.markdown(f"<div class='highlight'>Revenue for <b>{cat}</b> is <b>{rev:.2f}</b>.</div>", unsafe_allow_html=True)
else:
    chart = (
        alt.Chart(cat_data)
        .mark_bar(color=SECONDARY)
        .encode(
            x="product_category:N",
            y="line_revenue:Q",
            tooltip=["product_category", "line_revenue"]
        )
    )
    st.altair_chart(chart, use_container_width=True)

# --- STORE REVENUE ---
st.markdown("<div class='section-title'>Revenue by Store</div>", unsafe_allow_html=True)

store_filter = st.multiselect("Filter Store", df['store_location'].unique())

df_store = df.copy()
if store_filter:
    df_store = df_store[df_store['store_location'].isin(store_filter)]

store_data = df_store.groupby("store_location")["line_revenue"].sum().reset_index()

if len(store_filter) == 1:
    s = store_filter[0]
    rev = store_data.loc[store_data['store_location'] == s, 'line_revenue'].values[0]
    st.markdown(f"<div class='highlight'>Revenue for <b>{s}</b> store is <b>{rev:.2f}</b>.</div>", unsafe_allow_html=True)
else:
    chart = (
        alt.Chart(store_data)
        .mark_bar(color=ACCENT)
        .encode(
            x="store_location:N",
            y="line_revenue:Q",
            tooltip=["store_location", "line_revenue"]
        )
    )
    st.altair_chart(chart, use_container_width=True)

# --- TOP PRODUCTS ---
st.markdown("<div class='section-title'>Top Products</div>", unsafe_allow_html=True)

product_filter = st.multiselect("Filter Product Category", df['product_category'].unique())

df_prod = df.copy()
if product_filter:
    df_prod = df_prod[df_prod['product_category'].isin(product_filter)]

prod_data = (
    df_prod.groupby("product_name")["line_revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

if len(product_filter) == 1:
    st.markdown("<div class='highlight'>Showing top products for the selected category.</div>", unsafe_allow_html=True)

chart = (
    alt.Chart(prod_data)
    .mark_bar()
    .encode(
        x="line_revenue:Q",
        y=alt.Y("product_name:N", sort="-x"),
        color=alt.Color("line_revenue:Q", scale=alt.Scale(scheme="blues")),
        tooltip=["product_name", "line_revenue"]
    )
)
st.altair_chart(chart, use_container_width=True)

# --- TOP CUSTOMERS ---
st.markdown("<div class='section-title'>Top Customers</div>", unsafe_allow_html=True)

segment_filter = st.multiselect("Filter Customer Segment", df['customer_segment'].unique())

df_cust = df.copy()
if segment_filter:
    df_cust = df_cust[df_cust['customer_segment'].isin(segment_filter)]

cust_data = (
    df_cust.groupby("customer_id")["line_revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

if len(segment_filter) == 1:
    st.markdown("<div class='highlight'>Showing top customers for the selected segment.</div>", unsafe_allow_html=True)

chart = (
    alt.Chart(cust_data)
    .mark_circle()
    .encode(
        x="customer_id:N",
        y="line_revenue:Q",
        size=alt.Size("line_revenue:Q", scale=alt.Scale(range=[200, 2000])),
        color=alt.Color("line_revenue:Q", scale=alt.Scale(scheme="oranges")),
        tooltip=["customer_id", "line_revenue"]
    )
)
st.altair_chart(chart, use_container_width=True)
