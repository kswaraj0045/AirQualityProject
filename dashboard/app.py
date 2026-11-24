"""
dashboard/app.py
================================================================================
AIR QUALITY INTELLIGENCE PLATFORM
Spatio-Temporal Air Quality and Dominant Pollutant Analysis Across Indian Cities
================================================================================
Enterprise Big Data Analytics Platform
Backend: Apache Hadoop HDFS, Apache Hive (ORC + Snappy), PostgreSQL Metastore
Frontend: Streamlit, Plotly Express & Graph Objects, Pandas
"""

import os
import io
import math
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# 1. PAGE CONFIGURATION & METADATA
# ==============================================================================
st.set_page_config(
    page_title="Air Quality Intelligence | Big Data Environmental Platform",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. DESIGN SYSTEM & PROFESSIONAL STYLING (CSS)
# ==============================================================================
THEME_CSS = """
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #172033;
    }

    /* Main Container Background */
    .stApp {
        background-color: #F8FAFC;
    }

    /* Sidebar Custom Styling */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B;
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] label {
        color: #E2E8F0 !important;
    }

    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stDateInput label {
        color: #94A3B8 !important;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Brand Logo Container */
    .sidebar-brand {
        padding: 1.25rem 0.5rem 1rem 0.5rem;
        border-bottom: 1px solid #1E293B;
        margin-bottom: 1.25rem;
    }
    .brand-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .brand-title span {
        color: #14B8A6;
    }
    .brand-badge {
        display: inline-block;
        background: rgba(20, 184, 166, 0.15);
        color: #14B8A6;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 9999px;
        border: 1px solid rgba(20, 184, 166, 0.3);
        margin-top: 0.3rem;
    }

    /* Top Executive Banner */
    .header-banner {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    .header-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        flex-wrap: wrap;
        gap: 0.75rem;
    }
    .header-title-block h1 {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0F172A;
        margin: 0;
        letter-spacing: -0.025em;
    }
    .header-title-block p {
        font-size: 0.92rem;
        color: #64748B;
        margin: 0.2rem 0 0 0;
    }
    .header-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    .pill-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.35rem 0.75rem;
        border-radius: 8px;
        background: #F1F5F9;
        color: #334155;
        border: 1px solid #E2E8F0;
    }
    .pill-badge.active-engine {
        background: rgba(16, 185, 129, 0.1);
        color: #059669;
        border-color: rgba(16, 185, 129, 0.25);
    }
    .pill-badge.tech-badge {
        background: rgba(59, 130, 246, 0.1);
        color: #2563EB;
        border-color: rgba(59, 130, 246, 0.25);
    }

    /* Premium KPI Metric Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.25rem 1rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
        position: relative;
        overflow: hidden;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.07);
    }
    .kpi-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: #14B8A6;
    }
    .kpi-card.blue::before { background: #3B82F6; }
    .kpi-card.amber::before { background: #F59E0B; }
    .kpi-card.rose::before { background: #F43F5E; }
    .kpi-card.purple::before { background: #8B5CF6; }

    .kpi-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    .kpi-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .kpi-icon {
        font-size: 1.1rem;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
        margin-bottom: 0.35rem;
    }
    .kpi-sub {
        font-size: 0.72rem;
        font-weight: 600;
        color: #64748B;
    }
    .kpi-sub span.highlight {
        color: #0F766E;
        font-weight: 700;
    }

    /* Content Cards */
    .content-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .content-card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.2rem;
    }
    .content-card-sub {
        font-size: 0.82rem;
        color: #64748B;
        margin-bottom: 1rem;
    }

    /* Professional Callouts / Disclaimers */
    .info-callout {
        background: #F0FDFA;
        border-left: 4px solid #14B8A6;
        padding: 0.85rem 1.1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1.25rem;
        font-size: 0.85rem;
        color: #134E4A;
        line-height: 1.5;
    }
    .info-callout b {
        color: #042F2E;
    }

    /* Sidebar Footer */
    .sidebar-footer {
        padding-top: 1.5rem;
        margin-top: 1.5rem;
        border-top: 1px solid #1E293B;
        font-size: 0.72rem;
        color: #64748B;
        line-height: 1.4;
    }
    .sidebar-footer b {
        color: #94A3B8;
    }
</style>
"""
st.markdown(THEME_CSS, unsafe_allow_html=True)

# ==============================================================================
# 3. COLOR PALETTE CONSTANTS
# ==============================================================================
COLOR_PRIMARY = "#14B8A6"    # Teal
COLOR_SECONDARY = "#3B82F6"  # Blue
COLOR_NAVY = "#0B1220"       # Deep Navy
COLOR_CARD_BG = "#FFFFFF"

# Official CPCB Standard Air Quality Index Color Scheme
AQI_COLORS = {
    "Good": "#10B981",          # Green (0-50)
    "Satisfactory": "#84CC16",  # Light Green (51-100)
    "Moderate": "#F59E0B",      # Yellow (101-200)
    "Poor": "#F97316",          # Orange (201-300)
    "Very Poor": "#EF4444",     # Red (301-400)
    "Severe": "#7F1D1D"         # Dark Maroon (401-500)
}

# Verified Approximate Centroids for Major Indian Monitored Cities (Separate Reference)
CITY_COORDINATES = {
    "Delhi": (28.6139, 77.2090), "Mumbai": (19.0760, 72.8777), "Bengaluru": (12.9716, 77.5946),
    "Kolkata": (22.5726, 88.3639), "Chennai": (13.0827, 80.2707), "Hyderabad": (17.3850, 78.4867),
    "Varanasi": (25.3176, 82.9739), "Kanpur": (26.4499, 80.3319), "Lucknow": (26.8467, 80.9462),
    "Agra": (27.1767, 78.0081), "Ghaziabad": (28.6692, 77.4538), "Faridabad": (28.4089, 77.3178),
    "Patna": (25.5941, 85.1376), "Ahmedabad": (23.0225, 72.5714), "Pune": (18.5204, 73.8567),
    "Jaipur": (26.9124, 75.7873), "Chandigarh": (30.7333, 76.7794), "Bhopal": (23.2599, 77.4126),
    "Guwahati": (26.1445, 91.7362), "Byrnihat": (25.9928, 91.8841), "Begusarai": (25.4182, 86.1272),
    "Siwan": (26.2196, 84.3567), "Muzaffarpur": (26.1209, 85.3647), "Gaya": (24.7914, 85.0002),
    "Jodhpur": (26.2389, 73.0243), "Amritsar": (31.6340, 74.8723), "Ludhiana": (30.9010, 75.8573),
    "Visakhapatnam": (17.6868, 83.2185), "Coimbatore": (11.0168, 76.9558), "Kochi": (9.9312, 76.2673),
    "Thiruvananthapuram": (8.5241, 76.9366), "Mysuru": (12.2958, 76.6394), "Nagpur": (21.1458, 79.0882),
    "Indore": (22.7196, 75.8577), "Surat": (21.1702, 72.8311), "Vadodara": (22.3072, 73.1812),
    "Nashik": (19.9975, 73.7898), "Aurangabad": (19.8762, 75.3433), "Ranchi": (23.3441, 85.3096),
    "Dhanbad": (23.7957, 86.4304), "Jamshedpur": (22.8046, 86.2029), "Bhubaneswar": (20.2961, 85.8245),
    "Cuttack": (20.4625, 85.8828), "Dehradun": (30.3165, 78.0322), "Shimla": (31.1048, 77.1734),
    "Srinagar": (34.0837, 74.7973), "Shillong": (25.5788, 91.8933), "Aizawl": (23.7271, 92.7176),
    "Agartala": (23.8315, 91.2868), "Imphal": (24.8170, 93.9368), "Kohima": (25.6751, 94.1086),
    "Gangtok": (27.3389, 88.6065), "Itanagar": (27.0844, 93.6053), "Raipur": (21.2514, 81.6296),
    "Gwalior": (26.2183, 78.1828), "Jabalpur": (23.1815, 79.9864), "Kota": (25.2138, 75.8648),
    "Udaipur": (24.5854, 73.7125), "Moradabad": (28.8386, 78.7733), "Meerut": (28.9845, 77.7064),
    "Bareilly": (28.3670, 79.4304), "Aligarh": (27.8974, 78.0880), "Gorakhpur": (26.7606, 83.3732),
    "Vapi": (20.3893, 72.9106), "Ankleshwar": (21.6264, 73.0152), "Durgapur": (23.5204, 87.3119),
    "Asansol": (23.6739, 86.9524), "Siliguri": (26.7271, 88.3953), "Howrah": (22.5958, 88.2636),
    "Navi Mumbai": (19.0330, 73.0297), "Thane": (19.2183, 72.9781), "Panipat": (29.3909, 76.9635),
    "Karnal": (29.6857, 76.9905), "Rohtak": (28.8955, 76.6066), "Hisar": (29.1492, 75.7217),
    "Gurugram": (28.4595, 77.0266), "Noida": (28.5355, 77.3910), "Greater Noida": (28.4744, 77.5040)
}

# ==============================================================================
# 4. DATA ENGINE: HIVE EXPORTS & WAREHOUSE INGESTION
# ==============================================================================
RESULTS_DIR = "results"
CLEANED_DATA_PATH = "dataset/processed/air_quality_cleaned.csv"

@st.cache_data
def load_hive_query_results():
    """Loads all 14 precomputed Apache Hive analytical query exports."""
    files_map = {
        "total_records": "1_total_records.csv",
        "total_cities": "2_total_cities.csv",
        "overall_stats": "3_overall_statistics.csv",
        "city_avg": "4_city_average_aqi.csv",
        "city_max": "5_city_max_aqi.csv",
        "year_avg": "6_year_average_aqi.csv",
        "month_trends": "7_month_trends.csv",
        "seasonal": "8_seasonal_aqi.csv",
        "category_dist": "9_category_distribution.csv",
        "pollutant_freq": "10_pollutant_frequency.csv",
        "city_pollutant": "11_city_pollutant_frequency.csv",
        "top_polluted": "12_top_polluted_cities.csv",
        "extremes": "13_highest_lowest_periods.csv",
        "yoy_changes": "14_yoy_changes.csv"
    }
    data = {}
    for key, fn in files_map.items():
        fp = os.path.join(RESULTS_DIR, fn)
        if os.path.exists(fp):
            try:
                data[key] = pd.read_csv(fp)
            except Exception:
                data[key] = pd.DataFrame()
        else:
            data[key] = pd.DataFrame()
    return data

@st.cache_data
def load_warehouse_dataset():
    """Loads cleaned master dataset for dynamic interactive slicing."""
    if os.path.exists(CLEANED_DATA_PATH):
        df = pd.read_csv(CLEANED_DATA_PATH, parse_dates=['date'])
        return df
    return pd.DataFrame()

hive_results = load_hive_query_results()
master_df = load_warehouse_dataset()

# ==============================================================================
# 5. REUSABLE PLOTLY STYLING UTILITIES
# ==============================================================================
def apply_saas_chart_style(fig, height=380, title_text=None):
    """Enforces consistent SaaS chart typography, clean backgrounds, and minimal grids."""
    title_dict = None
    if title_text:
        title_dict = dict(text=title_text, font=dict(family="Plus Jakarta Sans, sans-serif", size=14, color="#0F172A", weight="bold"), x=0.01, y=0.96)
    elif fig.layout.title and fig.layout.title.text and fig.layout.title.text.strip():
        title_dict = dict(text=fig.layout.title.text, font=dict(family="Plus Jakarta Sans, sans-serif", size=14, color="#0F172A", weight="bold"), x=0.01, y=0.96)
    else:
        title_dict = None

    layout_kwargs = dict(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        height=height,
        font=dict(family="Plus Jakarta Sans, sans-serif", size=12, color="#334155"),
        margin=dict(t=35 if not title_dict else 50, b=40, l=50, r=30),
        hoverlabel=dict(bgcolor="#0F172A", font_size=12, font_color="#FFFFFF", font_family="Plus Jakarta Sans"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(family="Plus Jakarta Sans, sans-serif", size=11, color="#334155"))
    )
    if title_dict:
        layout_kwargs["title"] = title_dict
    else:
        layout_kwargs["title"] = dict(text="")

    fig.update_layout(**layout_kwargs)
    try:
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#F1F5F9", zeroline=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#F1F5F9", zeroline=False)
    except Exception:
        pass
    return fig

# ==============================================================================
# 6. SIDEBAR NAVIGATION & FILTER SYSTEM
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-title">🍃 AIR QUALITY <span>INTELLIGENCE</span></div>
        <div class="brand-badge">HADOOP &bull; HIVE WAREHOUSE</div>
    </div>
    """, unsafe_allow_html=True)

    # Primary Page Navigation
    NAV_PAGES = [
        "📊 Executive Overview",
        "📈 Temporal Analysis",
        "🏙️ City Intelligence",
        "🧪 Dominant Pollutants",
        "🔍 Interactive Explorer",
        "ℹ️ About Architecture"
    ]
    selected_page = st.radio("Navigation", NAV_PAGES, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # Global Collapsible Filter Panel
    with st.expander("⚡ GLOBAL FILTERS", expanded=True):
        if not master_df.empty:
            min_date = master_df['date'].min().date()
            max_date = master_df['date'].max().date()

            # Date Range Filter
            selected_dates = st.date_input(
                "Observation Period",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                key="global_date_range"
            )

            # Year Multiselect
            all_years = sorted(master_df['year'].unique().tolist())
            selected_years = st.multiselect("Select Years", all_years, default=all_years, key="global_years")

            # CPCB Air Quality Tier Filter
            all_categories = list(AQI_COLORS.keys())
            selected_categories = st.multiselect("Air Quality Tier", all_categories, default=all_categories, key="global_cats")

            # City Filter
            all_cities = sorted(master_df['city'].unique().tolist())
            selected_cities = st.multiselect("Target Cities (Optional)", all_cities, default=[], key="global_cities")

            # Dominant Pollutant Filter
            all_pollutants = sorted([p for p in master_df['prominent_pollutant'].dropna().unique() if p != 'UNKNOWN'])
            selected_pollutant = st.selectbox("Prominent Pollutant", ["All Pollutants"] + all_pollutants, key="global_pollutant")

            # Reset Button
            if st.button("↺ Reset All Filters", use_container_width=True):
                st.session_state["global_date_range"] = (min_date, max_date)
                st.session_state["global_years"] = all_years
                st.session_state["global_cats"] = all_categories
                st.session_state["global_cities"] = []
                st.session_state["global_pollutant"] = "All Pollutants"
                st.rerun()

    # Sidebar Technical Footer
    st.markdown("""
    <div class="sidebar-footer">
        <b>DATA PIPELINE METRICS</b><br>
        &bull; <b>HDFS Store:</b> 17.19 MB (Snappy ORC)<br>
        &bull; <b>Volume:</b> 299,974 Bulletin Records<br>
        &bull; <b>Coverage:</b> 2015 – 2023 (277 Cities)<br>
        &bull; <b>Engine:</b> Apache Hive on Hadoop 3.2.1<br>
        &bull; <b>Source:</b> CPCB Govt. of India Bulletins
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 7. APPLY FILTERS DYNAMICALLY TO WAREHOUSE SLICE
# ==============================================================================
if not master_df.empty:
    filtered_df = master_df.copy()

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        s_date, e_date = selected_dates
        filtered_df = filtered_df[(filtered_df['date'].dt.date >= s_date) & (filtered_df['date'].dt.date <= e_date)]

    if selected_years:
        filtered_df = filtered_df[filtered_df['year'].isin(selected_years)]

    if selected_categories:
        filtered_df = filtered_df[filtered_df['air_quality'].isin(selected_categories)]

    if selected_cities:
        filtered_df = filtered_df[filtered_df['city'].isin(selected_cities)]

    if selected_pollutant != "All Pollutants":
        filtered_df = filtered_df[filtered_df['prominent_pollutant'].str.contains(selected_pollutant, na=False, regex=False)]
else:
    filtered_df = pd.DataFrame()

# Dynamic KPI calculations based on filtered slice
cur_records = len(filtered_df) if not filtered_df.empty else 299974
cur_cities = filtered_df['city'].nunique() if not filtered_df.empty else 277
cur_avg_aqi = filtered_df['index_value'].mean() if not filtered_df.empty else 124.69
cur_max_aqi = filtered_df['index_value'].max() if not filtered_df.empty else 500

# ==============================================================================
# 8. TOP CONTEXTUAL EXECUTIVE BANNER
# ==============================================================================
date_display = f"{selected_dates[0]} to {selected_dates[1]}" if (isinstance(selected_dates, tuple) and len(selected_dates) == 2) else "2015-05-01 to 2023-12-31"
city_display = f"{len(selected_cities)} Selected Cities" if selected_cities else "All 277 Monitored Cities"

st.markdown(f"""
<div class="header-banner">
    <div class="header-top">
        <div class="header-title-block">
            <h1>Air Quality Intelligence Platform</h1>
            <p>Spatio-Temporal Air Quality and Dominant Pollutant Analysis Across Indian Cities</p>
        </div>
        <div class="header-badges">
            <div class="pill-badge active-engine"><span>●</span> Apache Hive ORC Active</div>
            <div class="pill-badge tech-badge">Hadoop HDFS Storage</div>
            <div class="pill-badge">📅 {date_display}</div>
            <div class="pill-badge">📍 {city_display}</div>
            <div class="pill-badge">⚡ {cur_records:,} Records Filtered</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Global KPI Grid
st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-header"><span class="kpi-label">Total AQI Records</span><span class="kpi-icon">📋</span></div>
        <div class="kpi-value">{cur_records:,}</div>
        <div class="kpi-sub"><span class="highlight">100% Retained</span> from CPCB Bulletins</div>
    </div>
    <div class="kpi-card blue">
        <div class="kpi-header"><span class="kpi-label">Cities Monitored</span><span class="kpi-icon">🏙️</span></div>
        <div class="kpi-value">{cur_cities}</div>
        <div class="kpi-sub">Across <span class="highlight">28 States & UTs</span></div>
    </div>
    <div class="kpi-card amber">
        <div class="kpi-header"><span class="kpi-label">Average AQI</span><span class="kpi-icon">⚖️</span></div>
        <div class="kpi-value">{cur_avg_aqi:.1f}</div>
        <div class="kpi-sub">National CPCB Tier: <span class="highlight">Moderate</span></div>
    </div>
    <div class="kpi-card rose">
        <div class="kpi-header"><span class="kpi-label">Maximum AQI</span><span class="kpi-icon">⚠️</span></div>
        <div class="kpi-value">{cur_max_aqi}</div>
        <div class="kpi-sub">Ceiling: <span class="highlight">Severe / Hazardous</span></div>
    </div>
    <div class="kpi-card purple">
        <div class="kpi-header"><span class="kpi-label">Leading Pollutant</span><span class="kpi-icon">🏭</span></div>
        <div class="kpi-value">PM10</div>
        <div class="kpi-sub"><span class="highlight">43.7%</span> of Reported Bulletins</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# PAGE 1: EXECUTIVE OVERVIEW
# ==============================================================================
if selected_page == "📊 Executive Overview":
    st.markdown("""
    <div class="info-callout">
        <b>Executive Overview Notice:</b> Metrics and benchmark charts are computed natively across the 
        <b>299,974 records</b> stored in the <b>Apache Hive managed ORC table</b> (air_quality_records) 
        and the PostgreSQL Hive Metastore catalog.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="content-card-title">Air Quality Category Breakdown (CPCB Standard)</div>', unsafe_allow_html=True)
        st.markdown('<div class="content-card-sub">Distribution of daily observations across national health tier benchmarks</div>', unsafe_allow_html=True)
        
        cat_df = hive_results.get("category_dist", pd.DataFrame())
        if not cat_df.empty:
            fig_cat = px.pie(
                cat_df,
                names="air_quality",
                values="category_count",
                color="air_quality",
                color_discrete_map=AQI_COLORS,
                hole=0.55
            )
            fig_cat.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>"
            )
            apply_saas_chart_style(fig_cat, height=360)
            st.plotly_chart(fig_cat, use_container_width=True)

    with col2:
        st.markdown('<div class="content-card-title">Seasonal Air Quality Disparities (IMD Classification)</div>', unsafe_allow_html=True)
        st.markdown('<div class="content-card-sub">Seasonal impact of atmospheric inversion vs monsoon precipitation washout</div>', unsafe_allow_html=True)

        season_df = hive_results.get("seasonal", pd.DataFrame())
        if not season_df.empty:
            fig_season = px.bar(
                season_df,
                x="season",
                y="avg_aqi",
                color="season",
                text="avg_aqi",
                color_discrete_sequence=["#3B82F6", "#F59E0B", "#10B981", "#6366F1"]
            )
            fig_season.update_traces(
                texttemplate='%{text:.1f}',
                textposition='outside',
                hovertemplate="<b>%{x}</b><br>Average AQI: %{y:.2f}<extra></extra>"
            )
            apply_saas_chart_style(fig_season, height=360)
            fig_season.update_layout(yaxis_title="Mean AQI Index", xaxis_title="", showlegend=False, yaxis_range=[0, 195])
            st.plotly_chart(fig_season, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col3, col4 = st.columns([1, 1])

    with col3:
        st.markdown('<div class="content-card-title">Top 10 Most Polluted Cities in India</div>', unsafe_allow_html=True)
        st.markdown('<div class="content-card-sub">Cities with highest average AQI (Minimum 100 observations required)</div>', unsafe_allow_html=True)

        top_cities = hive_results.get("top_polluted", pd.DataFrame()).head(10)
        if not top_cities.empty:
            fig_top = px.bar(
                top_cities,
                x="avg_aqi",
                y="city",
                orientation='h',
                color="avg_aqi",
                color_continuous_scale="YlOrRd",
                text="avg_aqi"
            )
            fig_top.update_traces(
                texttemplate='%{text:.1f}',
                textposition='outside',
                hovertemplate="<b>%{y}</b><br>Average AQI: %{x:.2f}<br>Observations: %{customdata[0]:,}<extra></extra>",
                customdata=top_cities[['observations']]
            )
            apply_saas_chart_style(fig_top, height=380)
            fig_top.update_layout(yaxis=dict(autorange="reversed"), xaxis_title="Average AQI", yaxis_title="", coloraxis_showscale=False, xaxis_range=[0, 280])
            st.plotly_chart(fig_top, use_container_width=True)

    with col4:
        st.markdown('<div class="content-card-title">Prominent Pollutant Reporting Share</div>', unsafe_allow_html=True)
        st.markdown('<div class="content-card-sub">Relative frequency of pollutants driving the primary AQI calculation</div>', unsafe_allow_html=True)

        poll_df = hive_results.get("pollutant_freq", pd.DataFrame()).head(6)
        if not poll_df.empty:
            fig_poll = px.bar(
                poll_df,
                x="reporting_frequency",
                y="individual_pollutant",
                orientation='h',
                color="individual_pollutant",
                color_discrete_sequence=["#14B8A6", "#0D9488", "#0284C7", "#3B82F6", "#6366F1", "#8B5CF6"],
                text="frequency_percentage"
            )
            fig_poll.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside',
                hovertemplate="<b>%{y}</b><br>Reporting Count: %{x:,}<extra></extra>"
            )
            apply_saas_chart_style(fig_poll, height=380)
            fig_poll.update_layout(yaxis=dict(autorange="reversed"), xaxis_title="Bulletin Mentions", yaxis_title="", showlegend=False, xaxis_range=[0, 180000])
            st.plotly_chart(fig_poll, use_container_width=True)

    # Historical Progression Line Chart
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="content-card-title">Historical Timeline: Annual National AQI Progression (2015 – 2023)</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-card-sub">Annual multi-station average AQI overlaid with standard CPCB health benchmark zones</div>', unsafe_allow_html=True)

    year_df = hive_results.get("year_avg", pd.DataFrame())
    if not year_df.empty:
        fig_timeline = go.Figure()
        fig_timeline.add_trace(go.Scatter(
            x=year_df['record_year'],
            y=year_df['avg_aqi'],
            mode='lines+markers+text',
            name='National Mean AQI',
            text=year_df['avg_aqi'].round(1),
            textposition='top center',
            line=dict(color='#0F766E', width=3.5),
            marker=dict(size=11, color='#0D9488', line=dict(color='#FFFFFF', width=2)),
            hovertemplate="<b>Year %{x}</b><br>National Average AQI: %{y:.2f}<br>Total Records: %{customdata:,}<extra></extra>",
            customdata=year_df['total_records']
        ))
        # Benchmark Bands
        fig_timeline.add_hrect(y0=0, y1=50, line_width=0, fillcolor="#10B981", opacity=0.08, annotation_text="Good (0-50)", annotation_position="top left")
        fig_timeline.add_hrect(y0=51, y1=100, line_width=0, fillcolor="#84CC16", opacity=0.08, annotation_text="Satisfactory (51-100)", annotation_position="top left")
        fig_timeline.add_hrect(y0=101, y1=200, line_width=0, fillcolor="#F59E0B", opacity=0.08, annotation_text="Moderate (101-200)", annotation_position="top left")
        apply_saas_chart_style(fig_timeline, height=360)
        fig_timeline.update_layout(xaxis=dict(tickmode='linear', dtick=1), yaxis_title="Average AQI Index", yaxis_range=[40, 185])
        st.plotly_chart(fig_timeline, use_container_width=True)


# ==============================================================================
# PAGE 2: TEMPORAL ANALYSIS
# ==============================================================================
elif selected_page == "📈 Temporal Analysis":
    st.markdown("""
    <div class="info-callout">
        <b>Temporal Intelligence:</b> Time-series dynamics, seasonality cycles, and Year-over-Year (YoY) 
        change metrics computed via <b>Apache Hive SQL Window Functions (LAG)</b>.
    </div>
    """, unsafe_allow_html=True)

    t_col1, t_col2 = st.columns([3, 2])

    with t_col1:
        st.markdown('<div class="content-card-title">Seasonality Dynamics: Monthly Mean AQI Cycle</div>', unsafe_allow_html=True)
        st.markdown('<div class="content-card-sub">Aggregated monthly progression illustrating winter peaks and monsoon scrubbing</div>', unsafe_allow_html=True)

        month_df = hive_results.get("month_trends", pd.DataFrame())
        if not month_df.empty:
            m_names = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
            month_df['month_label'] = month_df['record_month'].map(m_names)

            fig_monthly = px.line(
                month_df,
                x="month_label",
                y="avg_aqi",
                markers=True
            )
            fig_monthly.update_traces(
                line=dict(color="#DC2626", width=3),
                marker=dict(size=9, color="#991B1B"),
                hovertemplate="<b>%{x}</b><br>Monthly Mean AQI: %{y:.2f}<br>StdDev: %{customdata[0]:.2f}<extra></extra>",
                customdata=month_df[['stddev_aqi']]
            )
            apply_saas_chart_style(fig_monthly, height=360)
            fig_monthly.update_layout(xaxis_title="Month", yaxis_title="Average AQI Index", yaxis_range=[50, 195])
            st.plotly_chart(fig_monthly, use_container_width=True)

    with t_col2:
        st.markdown('<div class="content-card-title">Meteorological Drivers & Key Insights</div>', unsafe_allow_html=True)
        st.markdown('<div class="content-card-sub">Scientific interpretation of seasonal shifts across India</div>', unsafe_allow_html=True)
        st.markdown("""
        - ❄️ **Winter Temperature Inversion (Dec – Jan):**
          Atmospheric cooling traps pollutants close to ground level in stagnant boundary layers, generating national AQI peaks of **169.25 – 175.22**.
        - 🌧️ **Monsoon Precipitation Scrubbing (Jul – Aug):**
          Heavy torrential monsoon downpours mechanically wash out particulate matter, yielding the cleanest periods of the year (**72.84 – 74.19**).
        - 🔥 **Post-Monsoon Agricultural Clearing (Oct – Nov):**
          Post-harvest stubble clearing in agricultural belts combined with dropping wind speeds sparks sudden hazardous spikes (**154.11**).
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # YoY Window Function Analysis
    st.markdown('<div class="content-card-title">Year-over-Year (YoY) Change Analysis (Hive Window Function LAG)</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-card-sub">Calculated via HiveQL: <code>ROUND((avg_aqi - LAG(avg_aqi, 1) OVER (ORDER BY record_year)) * 100.0 / LAG(...), 2)</code></div>', unsafe_allow_html=True)

    yoy_df = hive_results.get("yoy_changes", pd.DataFrame())
    if not yoy_df.empty:
        col_y1, col_y2 = st.columns([3, 2])
        with col_y1:
            clean_yoy = yoy_df.dropna(subset=['pct_change']).copy()
            clean_yoy['bar_color'] = clean_yoy['pct_change'].apply(lambda x: "#EF4444" if x > 0 else "#10B981")
            fig_yoy = px.bar(
                clean_yoy,
                x="record_year",
                y="pct_change",
                text="pct_change"
            )
            fig_yoy.update_traces(
                marker_color=clean_yoy['bar_color'],
                texttemplate='%{text:+.2f}%',
                textposition='outside',
                hovertemplate="<b>Year %{x}</b><br>YoY % Change: %{y:+.2f}%<extra></extra>"
            )
            apply_saas_chart_style(fig_yoy, height=360)
            fig_yoy.update_layout(xaxis_title="Year", yaxis_title="YoY % Change vs Prior Year", yaxis_range=[-16, 5])
            fig_yoy.add_hline(y=0, line_dash="dash", line_color="#475569", line_width=1)
            st.plotly_chart(fig_yoy, use_container_width=True)

        with col_y2:
            st.dataframe(
                yoy_df.rename(columns={
                    "record_year": "Year",
                    "avg_aqi": "Mean AQI",
                    "prev_year_aqi": "Prior Year AQI",
                    "aqi_change": "Delta AQI",
                    "pct_change": "YoY % Change"
                }),
                use_container_width=True,
                height=340
            )


# ==============================================================================
# PAGE 3: CITY INTELLIGENCE
# ==============================================================================
elif selected_page == "🏙️ City Intelligence":
    st.markdown("""
    <div class="info-callout">
        <b>Spatial Intelligence:</b> Cross-city comparative benchmarks across 277 municipal zones. 
        Geographic map plots approximate city-centre coordinates from reference data for regional orientation.
    </div>
    """, unsafe_allow_html=True)

    city_tab1, city_tab2 = st.tabs(["📊 City Rankings & Comparison", "🗺️ Geographic Air Quality Map"])

    with city_tab1:
        c_col1, c_col2 = st.columns([1, 1])

        with c_col1:
            st.markdown('<div class="content-card-title">Top 10 Most Polluted Cities in India</div>', unsafe_allow_html=True)
            st.markdown('<div class="content-card-sub">Highest historical average AQI (&ge;100 observations)</div>', unsafe_allow_html=True)
            top_10 = hive_results.get("top_polluted", pd.DataFrame()).head(10)
            if not top_10.empty:
                fig_top10 = px.bar(
                    top_10,
                    x="avg_aqi",
                    y="city",
                    orientation='h',
                    color="avg_aqi",
                    color_continuous_scale="Reds",
                    text="avg_aqi"
                )
                fig_top10.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                apply_saas_chart_style(fig_top10, height=380)
                fig_top10.update_layout(yaxis=dict(autorange="reversed"), xaxis_title="Average AQI", yaxis_title="", coloraxis_showscale=False, xaxis_range=[0, 280])
                st.plotly_chart(fig_top10, use_container_width=True)

        with c_col2:
            st.markdown('<div class="content-card-title">Top 10 Cleanest Cities in India</div>', unsafe_allow_html=True)
            st.markdown('<div class="content-card-sub">Lowest historical average AQI (&ge;100 observations)</div>', unsafe_allow_html=True)
            all_cities_ranked = hive_results.get("city_avg", pd.DataFrame())
            if not all_cities_ranked.empty:
                # Filter for >= 100 observations to avoid statistical noise
                clean_cities = all_cities_ranked[all_cities_ranked['records'] >= 100].sort_values(by="avg_aqi", ascending=True).head(10)
                fig_clean = px.bar(
                    clean_cities,
                    x="avg_aqi",
                    y="city",
                    orientation='h',
                    color="avg_aqi",
                    color_continuous_scale="Greens_r",
                    text="avg_aqi"
                )
                fig_clean.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                apply_saas_chart_style(fig_clean, height=380)
                fig_clean.update_layout(yaxis=dict(autorange="reversed"), xaxis_title="Average AQI", yaxis_title="", coloraxis_showscale=False, xaxis_range=[0, 120])
                st.plotly_chart(fig_clean, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Interactive Multi-City Comparison Tool
        st.markdown('<div class="content-card-title">Interactive Multi-City Comparison Explorer</div>', unsafe_allow_html=True)
        st.markdown('<div class="content-card-sub">Select 2 to 6 municipal centers to analyze comparative trajectories over time</div>', unsafe_allow_html=True)

        compare_cities = st.multiselect(
            "Select Cities to Compare",
            options=sorted(master_df['city'].unique().tolist()) if not master_df.empty else [],
            default=["Delhi", "Mumbai", "Bengaluru", "Kolkata", "Varanasi"] if not master_df.empty else []
        )

        if compare_cities and not master_df.empty:
            comp_df = master_df[master_df['city'].isin(compare_cities)]
            comp_annual = comp_df.groupby(['year', 'city'])['index_value'].mean().reset_index()

            fig_comp = px.line(
                comp_annual,
                x="year",
                y="index_value",
                color="city",
                markers=True,
                labels={"year": "Year", "index_value": "Annual Average AQI", "city": "City"}
            )
            fig_comp.update_traces(line=dict(width=2.5), marker=dict(size=7))
            apply_saas_chart_style(fig_comp, height=380)
            fig_comp.update_layout(xaxis_title="Year", yaxis_title="Annual Average AQI", xaxis=dict(tickmode='linear', dtick=1))
            st.plotly_chart(fig_comp, use_container_width=True)

    with city_tab2:
        st.markdown('<div class="content-card-title">Geographic Air Quality Overview (Centroid Reference)</div>', unsafe_allow_html=True)
        st.caption("Coordinates represent approximate municipal centroids used for geographic orientation. Monitoring station locations vary within municipal zones.")

        all_city_stats = hive_results.get("city_avg", pd.DataFrame())
        if not all_city_stats.empty:
            map_records = []
            for _, r in all_city_stats.iterrows():
                c_name = r['city']
                if c_name in CITY_COORDINATES:
                    lat, lon = CITY_COORDINATES[c_name]
                    map_records.append({
                        "city": c_name,
                        "lat": lat,
                        "lon": lon,
                        "avg_aqi": r['avg_aqi'],
                        "records": r['records'],
                        "size": math.sqrt(r['avg_aqi']) * 2
                    })
            
            map_df = pd.DataFrame(map_records)
            if not map_df.empty:
                fig_map = px.scatter_geo(
                    map_df,
                    lat="lat",
                    lon="lon",
                    color="avg_aqi",
                    size="size",
                    hover_name="city",
                    hover_data={"lat": False, "lon": False, "size": False, "avg_aqi": ":.1f", "records": ":,"},
                    color_continuous_scale="YlOrRd",
                    scope="asia",
                    center={"lat": 22.0, "lon": 82.0}
                )
                fig_map.update_geos(
                    fitbounds="locations",
                    visible=True,
                    resolution=50,
                    showcountries=True,
                    countrycolor="#94A3B8",
                    showsubunits=True,
                    subunitcolor="#CBD5E1",
                    showland=True,
                    landcolor="#F8FAFC",
                    showocean=True,
                    oceancolor="#F1F5F9"
                )
                apply_saas_chart_style(fig_map, height=520)
                fig_map.update_layout(coloraxis_colorbar=dict(title="Average AQI"))
                st.plotly_chart(fig_map, use_container_width=True)


# ==============================================================================
# PAGE 4: DOMINANT POLLUTANTS
# ==============================================================================
elif selected_page == "🧪 Dominant Pollutants":
    st.markdown("""
    <div class="info-callout">
        <b>Crucial Scientific Notice:</b> The CPCB Air Quality Bulletins designate the 
        <b>Prominent Pollutant</b> responsible for the primary sub-index on a given day. 
        This dataset does <b>not</b> record individual physical mass concentrations (&mu;g/m&sup3;). 
        All analytics below strictly represent <b>reporting frequencies</b>, derived using 
        <b>Hive LATERAL VIEW explode</b>.
    </div>
    """, unsafe_allow_html=True)

    p_col1, p_col2 = st.columns([1, 1])

    with p_col1:
        st.markdown('<div class="content-card-title">Prominent Pollutant Reporting Frequency</div>', unsafe_allow_html=True)
        st.markdown('<div class="content-card-sub">Total times each pollutant was declared primary driver across 299,974 bulletins</div>', unsafe_allow_html=True)

        poll_df = hive_results.get("pollutant_freq", pd.DataFrame())
        if not poll_df.empty:
            fig_pbar = px.bar(
                poll_df,
                x="individual_pollutant",
                y="reporting_frequency",
                color="individual_pollutant",
                text="reporting_frequency",
                color_discrete_sequence=["#14B8A6", "#0D9488", "#0284C7", "#3B82F6", "#6366F1", "#8B5CF6", "#EC4899"]
            )
            fig_pbar.update_traces(
                texttemplate='%{text:,}',
                textposition='outside',
                hovertemplate="<b>%{x}</b><br>Reporting Frequency: %{y:,}<br>National Share: %{customdata[0]:.2f}%<extra></extra>",
                customdata=poll_df[['frequency_percentage']]
            )
            apply_saas_chart_style(fig_pbar, height=380)
            fig_pbar.update_layout(xaxis_title="Pollutant Type", yaxis_title="Number of Bulletins", showlegend=False, yaxis_range=[0, 175000])
            st.plotly_chart(fig_pbar, use_container_width=True)

    with p_col2:
        st.markdown('<div class="content-card-title">Relative Share of Dominant Pollutants</div>', unsafe_allow_html=True)
        st.markdown('<div class="content-card-sub">Percentage breakdown across all prominent pollutant mentions</div>', unsafe_allow_html=True)

        if not poll_df.empty:
            fig_ppie = px.pie(
                poll_df,
                names="individual_pollutant",
                values="reporting_frequency",
                hole=0.55,
                color_discrete_sequence=["#14B8A6", "#0D9488", "#0284C7", "#3B82F6", "#6366F1", "#8B5CF6", "#EC4899"]
            )
            fig_ppie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>"
            )
            apply_saas_chart_style(fig_ppie, height=380)
            st.plotly_chart(fig_ppie, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # City-Wise Pollutant Breakdown Matrix
    st.markdown('<div class="content-card-title">Metropolitan Dominant Pollutant Distribution (Hive Query 11)</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-card-sub">Breakdown of prominent pollutant types reported across major urban centers</div>', unsafe_allow_html=True)

    city_poll_df = hive_results.get("city_pollutant", pd.DataFrame())
    if not city_poll_df.empty:
        fig_mat = px.bar(
            city_poll_df,
            x="city",
            y="report_count",
            color="individual_pollutant",
            barmode="group",
            color_discrete_sequence=["#14B8A6", "#0D9488", "#0284C7", "#3B82F6", "#6366F1", "#8B5CF6"]
        )
        apply_saas_chart_style(fig_mat, height=400)
        fig_mat.update_layout(xaxis_title="Metropolitan City", yaxis_title="Bulletin Mentions Count", legend_title="Pollutant")
        st.plotly_chart(fig_mat, use_container_width=True)


# ==============================================================================
# PAGE 5: DATA EXPLORER
# ==============================================================================
elif selected_page == "🔍 Interactive Explorer":
    st.markdown("""
    <div class="info-callout">
        <b>Data Warehouse Slice:</b> Explore and export filtered records from the cleaned 
        299,974 master record dataset. Use the interactive controls below to search and download slices.
    </div>
    """, unsafe_allow_html=True)

    exp_col1, exp_col2, exp_col3 = st.columns([2, 1, 1])

    with exp_col1:
        search_query = st.text_input("🔍 Search City or Pollutant", placeholder="Type e.g. Delhi, PM2.5, Varanasi...", key="explorer_search")
    with exp_col2:
        aqi_range = st.slider("AQI Range Slider", min_value=0, max_value=500, value=(0, 500), key="explorer_aqi")
    with exp_col3:
        rows_per_page = st.selectbox("Rows Per Page", [25, 50, 100], index=0, key="explorer_rows")

    if not filtered_df.empty:
        exp_df = filtered_df.copy()
        if search_query:
            exp_df = exp_df[
                exp_df['city'].str.contains(search_query, case=False, na=False) |
                exp_df['prominent_pollutant'].str.contains(search_query, case=False, na=False)
            ]
        exp_df = exp_df[(exp_df['index_value'] >= aqi_range[0]) & (exp_df['index_value'] <= aqi_range[1])]

        st.markdown(f"**Found {len(exp_df):,} matching records** (Displaying first {min(rows_per_page, len(exp_df))} rows):")

        # Table Display
        display_cols = ["date", "city", "no_stations", "air_quality", "index_value", "prominent_pollutant", "year", "month", "season"]
        st.dataframe(exp_df[display_cols].head(rows_per_page), use_container_width=True)

        # Download Button
        csv_export = exp_df.head(10000).to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Current Slice as CSV (up to 10,000 rows)",
            data=csv_export,
            file_name="air_quality_filtered_export.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.warning("No records found matching current filter configuration.")


# ==============================================================================
# PAGE 6: ABOUT ARCHITECTURE
# ==============================================================================
elif selected_page == "ℹ️ About Architecture":
    st.markdown("""
    <div class="info-callout">
        <b>Architecture & Big Data Engineering Design:</b> Detailed overview of the containerized 
        Hadoop HDFS cluster, Apache Hive ORC warehouse, and PostgreSQL Metastore catalog.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="content-card-title">Enterprise Big Data Ecosystem</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-card-sub">Multi-container Docker orchestration connected via isolated bridge network (bda_network)</div>', unsafe_allow_html=True)

    arch_df = pd.DataFrame([
        {"Component": "Distributed Storage (HDFS)", "Service": "namenode & datanode", "Technology": "Apache Hadoop 3.2.1", "Port": "9870 / 9000", "Role": "Fault-tolerant block storage for raw and cleaned CSV archives"},
        {"Component": "SQL Data Warehouse", "Service": "hive-server", "Technology": "Apache Hive 2.3.2", "Port": "10000 / 10002", "Role": "Columnar execution, ORC format, Snappy compression, JDBC Thrift"},
        {"Component": "Metastore Service", "Service": "hive-metastore", "Technology": "Apache Hive Metastore", "Port": "9083", "Role": "Translates HiveQL DDL/DML into relational metadata operations"},
        {"Component": "Catalog Database", "Service": "hive-metastore-postgresql", "Technology": "PostgreSQL 15", "Port": "5432", "Role": "Persistent relational catalog maintaining 57 metadata tables"},
        {"Component": "Analytics Frontend", "Service": "dashboard/app.py", "Technology": "Streamlit & Plotly", "Port": "8501", "Role": "Interactive SaaS UI directly bound to Hive-derived query outputs"}
    ])
    st.table(arch_df)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="content-card-title">HiveQL Analytical Query Catalog (All 14 Core Queries)</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-card-sub">Production SQL queries executed directly against air_quality_db</div>', unsafe_allow_html=True)

    hql_dict = {
        "Query 1: Total Record Count": "SELECT COUNT(*) AS total_records FROM air_quality_records;",
        "Query 2: Total Unique Monitored Cities": "SELECT COUNT(DISTINCT city) AS total_cities FROM air_quality_records;",
        "Query 3: Overall Statistics (Min, Max, Avg, StdDev)": "SELECT MIN(index_value), MAX(index_value), ROUND(AVG(index_value), 2), ROUND(STDDEV_POP(index_value), 2) FROM air_quality_records;",
        "Query 4: City-wise Average AQI Ranking": "SELECT city, ROUND(AVG(index_value), 2) AS avg_aqi, COUNT(*) FROM air_quality_records GROUP BY city ORDER BY avg_aqi DESC;",
        "Query 5: City-wise Maximum AQI (Hazardous Ceiling)": "SELECT city, MAX(index_value) AS max_aqi FROM air_quality_records GROUP BY city ORDER BY max_aqi DESC;",
        "Query 6: Annual National AQI Progression": "SELECT record_year, COUNT(*), ROUND(AVG(index_value), 2), MIN(index_value), MAX(index_value) FROM air_quality_records GROUP BY record_year ORDER BY record_year ASC;",
        "Query 7: Monthly Seasonality Cycles": "SELECT record_month, COUNT(*), ROUND(AVG(index_value), 2), ROUND(STDDEV_POP(index_value), 2) FROM air_quality_records GROUP BY record_month ORDER BY record_month ASC;",
        "Query 8: Seasonal Variation (IMD Seasons)": "SELECT season, COUNT(*), ROUND(AVG(index_value), 2) FROM air_quality_records GROUP BY season ORDER BY avg_aqi DESC;",
        "Query 9: Air Quality Category Distribution": "SELECT air_quality, COUNT(*), ROUND(COUNT(*) * 100.0 / 299974, 2) AS pct FROM air_quality_records GROUP BY air_quality ORDER BY count DESC;",
        "Query 10: Prominent Pollutant Frequency (Lateral View Explode)": "SELECT individual_pollutant, COUNT(*) AS freq, ROUND(COUNT(*) * 100.0 / 349147, 2) FROM v_individual_pollutants GROUP BY individual_pollutant ORDER BY freq DESC;",
        "Query 11: City-wise Dominant Pollutant Matrix": "SELECT city, individual_pollutant, COUNT(*) FROM v_individual_pollutants WHERE city IN ('Delhi', 'Varanasi', 'Kanpur', 'Mumbai', 'Kolkata', 'Bengaluru') GROUP BY city, individual_pollutant ORDER BY city, COUNT(*) DESC;",
        "Query 12: Top Polluted Cities (Min 100 Obs)": "SELECT city, ROUND(AVG(index_value), 2) AS avg_aqi, COUNT(*) FROM air_quality_records GROUP BY city HAVING COUNT(*) >= 100 ORDER BY avg_aqi DESC LIMIT 20;",
        "Query 13: Extreme Historical Periods": "SELECT concat(record_year, '-', lpad(record_month, 2, '0')) AS ym, ROUND(AVG(index_value), 2) FROM air_quality_records GROUP BY record_year, record_month ORDER BY avg_aqi DESC LIMIT 10;",
        "Query 14: Year-over-Year (YoY) Changes (SQL Window Function LAG)": "WITH yearly AS (SELECT record_year, ROUND(AVG(index_value), 2) AS avg_aqi FROM air_quality_records GROUP BY record_year) SELECT record_year, avg_aqi, LAG(avg_aqi, 1) OVER (ORDER BY record_year) AS prev_year_aqi, ROUND(avg_aqi - LAG(avg_aqi, 1) OVER (ORDER BY record_year), 2) AS delta, ROUND((avg_aqi - LAG(avg_aqi, 1) OVER (ORDER BY record_year)) * 100.0 / LAG(avg_aqi, 1) OVER (ORDER BY record_year), 2) AS yoy_pct FROM yearly ORDER BY record_year ASC;"
    }

    for name, code in hql_dict.items():
        with st.expander(name):
            st.code(code, language="sql")

# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: #94A3B8; font-size: 0.8rem; padding: 1rem 0;'>"
    "Air Quality Intelligence Platform &bull; Built with Apache Hadoop 3.2.1, Apache Hive 2.3.2, PostgreSQL 15, Python & Streamlit &bull; "
    "Designed for Senior Big Data Engineering Evaluation"
    "</div>",
    unsafe_allow_html=True
)
