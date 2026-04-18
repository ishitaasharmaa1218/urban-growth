import streamlit as st
import pandas as pd
import plotly.express as px
from utils.model import load_model

st.set_page_config(page_title="Urban Growth AI", layout="wide")

# ---------- PREMIUM CSS ----------
st.markdown("""
<style>

body {
    background-color: #0e1117;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #020617);
    color: white;
}

.main-title {
    font-size: 42px;
    font-weight: bold;
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(0,0,0,0.3);
}

.section {
    margin-top: 25px;
}

</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown('<div class="main-title">🌆 Urban Growth Intelligence AI</div>', unsafe_allow_html=True)
st.caption("Smart analytics for city growth and real estate trends")

# ---------- LOAD DATA ----------
df = pd.read_csv("data/urban_growth_dataset.csv")

# Add state mapping
city_state_map = {
    "Mumbai": "Maharashtra",
    "Pune": "Maharashtra",
    "Delhi": "Delhi",
    "Bangalore": "Karnataka",
    "Hyderabad": "Telangana",
    "Chennai": "Tamil Nadu",
    "Kolkata": "West Bengal",
    "Ahmedabad": "Gujarat",
    "Jaipur": "Rajasthan",
    "Chandigarh": "Punjab"
}

if "state" not in df.columns:
    df["state"] = df["city"].map(city_state_map)

# ---------- SIDEBAR ----------
st.sidebar.markdown("## 🌍 Control Panel")
st.sidebar.markdown("Customize your analysis")

states = st.sidebar.multiselect(
    "Select State",
    df["state"].unique(),
    default=df["state"].unique()
)

filtered_df = df[df["state"].isin(states)]

cities = st.sidebar.multiselect(
    "Select City",
    filtered_df["city"].unique(),
    default=filtered_df["city"].unique()
)

filtered_df = filtered_df[filtered_df["city"].isin(cities)]

st.sidebar.markdown("---")

# Prediction
st.sidebar.markdown("## 🔮 Growth Predictor")

population = st.sidebar.slider("Population", 100000, 10000000, 500000)
price_index = st.sidebar.slider("Price Index", 50, 500, 200)
infra_score = st.sidebar.slider("Infrastructure", 1, 10, 5)
employment_rate = st.sidebar.slider("Employment Rate", 40, 100, 70)

model = load_model()
prediction = model.predict([[population, price_index, infra_score, employment_rate]])

st.sidebar.success(f"Growth Score: {round(prediction[0], 2)}")

# ---------- KPI CARDS ----------
col1, col2, col3 = st.columns(3)

col1.markdown(f'<div class="card">📊 Total Cities<br><h2>{len(filtered_df)}</h2></div>', unsafe_allow_html=True)

col2.markdown(f'<div class="card">📈 Avg Price Index<br><h2>{round(filtered_df["price_index"].mean(),2)}</h2></div>', unsafe_allow_html=True)

top_city = filtered_df.sort_values("price_index", ascending=False).iloc[0]["city"]
col3.markdown(f'<div class="card">🏆 Top City<br><h2>{top_city}</h2></div>', unsafe_allow_html=True)

# ---------- MAP ----------
st.markdown('<div class="section"></div>', unsafe_allow_html=True)
st.subheader("🗺️ Growth Hotspot Map")

fig_map = px.scatter_mapbox(
    filtered_df,
    lat="lat",
    lon="lon",
    size="price_index",
    color="price_index",
    hover_name="city",
    zoom=3,
    mapbox_style="carto-darkmatter"
)

st.plotly_chart(fig_map, use_container_width=True)

# ---------- CHARTS ----------
st.markdown('<div class="section"></div>', unsafe_allow_html=True)
st.subheader("📊 Advanced Analytics")

col1, col2 = st.columns(2)

with col1:
    fig_bar = px.bar(
        filtered_df,
        x="city",
        y="price_index",
        color="state",
        template="plotly_dark"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    fig_scatter = px.scatter(
        filtered_df,
        x="population",
        y="price_index",
        size="infra_score",
        color="employment_rate",
        template="plotly_dark"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ---------- INSIGHTS ----------
st.markdown('<div class="section"></div>', unsafe_allow_html=True)
st.subheader("🔍 AI Insights")

top_city = filtered_df.sort_values("price_index", ascending=False).iloc[0]["city"]
low_city = filtered_df.sort_values("price_index").iloc[0]["city"]

col1, col2 = st.columns(2)

col1.markdown(f'<div class="card">🔥 Fastest Growing<br><h3>{top_city}</h3></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="card">📉 Slowest Growth<br><h3>{low_city}</h3></div>', unsafe_allow_html=True)