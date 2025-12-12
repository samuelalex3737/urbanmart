import streamlit as st
import pandas as pd
import altair as alt

# Load data
df = pd.read_csv("transactions_1000.csv")
df['date'] = pd.to_datetime(df['date'], format="%d-%m-%Y")
df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
df['day_of_week'] = df['date'].dt.day_name()

# --- Dashboard Styling ---
st.set_page_config(page_title="UrbanMart Dashboard", layout="wide")

PRIMARY_COLOR = "#4CAF50"
SECONDARY_COLOR = "#2196F3"
ACCENT_COLOR = "#FF9800"

st.markdown(
    f"""
    <style>
        .metric-box {{
            background-color: #f7f7f7;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid {PRIMARY_COLOR};
        }}
        .section-title {{
            font-size: 22px;
            font-weight: 600;
            color: {PRIMARY_COLOR};
            margin-top: 30px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Title ---
st.title("UrbanMart Sales Intelligence Dashboard")
st.write("A professional analytics dashboard built for executive insights.")

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

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Revenue by Category",
    "Revenue by Store",
    "Top Products",
    "Top Customers"
])

# --- TAB 1: Revenue by Category ---
with tab1:
    st.markdown("<div class='section-title'>Revenue by Product Category</div>", unsafe_allow_html=True)

    category_filter = st.multiselect(
        "Filter Categories",
        df['product_category'].unique()
    )

    df_cat = df.copy()
    if category_filter:
        df_cat = df_cat[df_cat['product_category'].isin(category_filter)]

    cat_data = df_cat.groupby("product_category")["line_revenue"].sum().reset_index()

    chart = (
        alt.Chart(cat_data)
        .mark_bar(color=PRIMARY_COLOR)
        .encode(
            x=alt.X("line_revenue:Q", title="Revenue"),
            y=alt.Y("product_category:N", sort="-x", title="Category"),
            tooltip=["product_category", "line_revenue"]
        )
        .properties(height=400)
    )

    st.altair_chart(chart, use_container_width=True)

# --- TAB 2: Revenue by Store ---
with tab2:
    st.markdown("<div class='section-title'>Revenue by Store Location</div>", unsafe_allow_html=True)

    store_filter = st.multiselect(
        "Filter Store Locations",
        df['store_location'].unique()
    )

    df_store = df.copy()
    if store_filter:
        df_store = df_store[df_store['store_location'].isin(store_filter)]

    store_data = df_store.groupby("store_location")["line_revenue"].sum().reset_index()

    chart = (
        alt.Chart(store_data)
        .mark_bar()
        .encode(
            x=alt.X("store_location:N", title="Store"),
            y=alt.Y("line_revenue:Q", title="Revenue"),
            color=alt.Color("store_location:N", scale=alt.Scale(scheme="tableau10")),
            tooltip=["store_location", "line_revenue"]
        )
        .properties(height=400)
    )

    st.altair_chart(chart, use_container_width=True)

# --- TAB 3: Top Products ---
with tab3:
    st.markdown("<div class='section-title'>Top 5 Products by Revenue</div>", unsafe_allow_html=True)

    product_filter = st.multiselect(
        "Filter Product Categories",
        df['product_category'].unique()
    )

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

    chart = (
        alt.Chart(prod_data)
        .mark_bar()
        .encode(
            x=alt.X("line_revenue:Q", title="Revenue"),
            y=alt.Y("product_name:N", sort="-x", title="Product"),
            color=alt.Color("line_revenue:Q", scale=alt.Scale(scheme="blues")),
            tooltip=["product_name", "line_revenue"]
        )
        .properties(height=400)
    )

    st.altair_chart(chart, use_container_width=True)

# --- TAB 4: Top Customers ---
with tab4:
    st.markdown("<div class='section-title'>Top 5 Customers by Revenue</div>", unsafe_allow_html=True)

    segment_filter = st.multiselect(
        "Filter Customer Segment",
        df['customer_segment'].unique()
    )

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

    chart = (
        alt.Chart(cust_data)
        .mark_circle()
        .encode(
            x=alt.X("customer_id:N", title="Customer"),
            y=alt.Y("line_revenue:Q", title="Revenue"),
            size=alt.Size("line_revenue:Q", scale=alt.Scale(range=[100, 2000])),
            color=alt.Color("line_revenue:Q", scale=alt.Scale(scheme="oranges")),
            tooltip=["customer_id", "line_revenue"]
        )
        .properties(height=400)
    )

    st.altair_chart(chart, use_container_width=True)
