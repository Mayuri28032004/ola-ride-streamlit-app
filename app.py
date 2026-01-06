import streamlit as st
import pandas as pd

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Ola Ride Insights",
    page_icon="🚖",
    layout="wide"
)

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("ola_rides.csv")
    return df

df = load_data()

# -------------------------------
# App Title
# -------------------------------
st.title("🚖 Ola Ride Insights Dashboard")
st.markdown("Interactive analysis of Ola ride bookings, revenue, and ratings.")

# -------------------------------
# Sidebar Filters
# -------------------------------
search_booking = st.sidebar.text_input("🔎 Search Booking ID")

if search_booking:
    df = df[df["Booking_Id"].astype(str).str.contains(search_booking)]

st.sidebar.header("🔍 Filters")

vehicle = st.sidebar.multiselect(
    "Select Vehicle Type",
    options=df["Vehicle_Type"].unique()
)

status = st.sidebar.multiselect(
    "Select Booking Status",
    options=df["Booking_Status"].unique()
)

payment = st.sidebar.multiselect(
    "Select Payment Method",
    options=df["Payment_Method"].unique()
)

# Apply filters
if vehicle:
    df = df[df["Vehicle_Type"].isin(vehicle)]

if status:
    df = df[df["Booking_Status"].isin(status)]

if payment:
    df = df[df["Payment_Method"].isin(payment)]

# -------------------------------
# KPIs
# -------------------------------
st.subheader("📊 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("Total Rides", df.shape[0])
col2.metric("Total Revenue", f"₹ {int(df['Booking_Value'].sum())}")
col3.metric("Avg Customer Rating", round(df["Customer_Rating"].mean(), 2))

# -------------------------------
# Charts
# -------------------------------
st.subheader("📈 Visual Analysis")

col4, col5 = st.columns(2)

# Rides Over Time
with col4:
    st.markdown("### Ride Volume Over Time")
    st.line_chart(
        df.groupby("Booking_Date")["Booking_Id"].count()
    )

# Revenue by Payment Method
with col5:
    st.markdown("### Revenue by Payment Method")
    st.bar_chart(
        df.groupby("Payment_Method")["Booking_Value"].sum()
    )

# -------------------------------
# Ratings Analysis
# -------------------------------
st.subheader("⭐ Ratings Analysis")

col6, col7 = st.columns(2)

with col6:
    st.markdown("### Avg Customer Rating by Vehicle Type")
    st.bar_chart(
        df.groupby("Vehicle_Type")["Customer_Rating"].mean()
    )

with col7:
    st.markdown("### Driver Ratings Distribution")
    st.bar_chart(
        df["Driver_Ratings"].value_counts().sort_index()
    )

# -------------------------------
# Data Table
# -------------------------------
st.subheader("📋 Detailed Ride Data")
st.dataframe(df)

# -------------------------------
# Download Filtered Data
# -------------------------------
st.subheader("⬇️ Download Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_ola_rides.csv",
    mime="text/csv"
)

# -------------------------------
# Power BI Dashboard Embed
# -------------------------------
st.subheader("📊 Power BI Dashboard")

st.write("Image file loaded successfully")
st.image("powerbi_Dashboard.png")
width=1100,
height=600

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("📌 **Project:** Ola Ride Insights | Built using Streamlit & Python")
