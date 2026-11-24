"""
scripts/generate_charts.py
Generates high-resolution PNG charts from Hive query outputs for documentation and Word report.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

CHARTS_DIR = "results/charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.size'] = 11

def chart_1_category_distribution():
    df = pd.read_csv("results/9_category_distribution.csv")
    colors = ['#84CC16', '#EAB308', '#22C55E', '#F97316', '#EF4444', '#7F1D1D']
    
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    wedges, texts, autotexts = ax.pie(
        df['category_count'],
        labels=df['air_quality'],
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        wedgeprops=dict(width=0.45, edgecolor='w')
    )
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')
    ax.set_title("CPCB Air Quality Category Distribution (2015 - 2023)", fontsize=14, weight='bold', pad=20)
    plt.tight_layout()
    out = os.path.join(CHARTS_DIR, "aqi_category_distribution.png")
    plt.savefig(out)
    plt.close()
    print(f"Generated: {out}")

def chart_2_seasonal_aqi():
    df = pd.read_csv("results/8_seasonal_aqi.csv")
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    bars = ax.bar(df['season'], df['avg_aqi'], color=['#3B82F6', '#F59E0B', '#10B981', '#6366F1'], width=0.55)
    
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 3, f"{yval:.1f}", ha='center', va='bottom', weight='bold')

    ax.set_ylabel("Average AQI Value", fontsize=12, weight='bold')
    ax.set_xlabel("Meteorological Season (IMD)", fontsize=12, weight='bold')
    ax.set_title("Seasonal Air Quality Variation across India (Hive Managed ORC)", fontsize=14, weight='bold', pad=15)
    ax.set_ylim(0, 200)
    plt.tight_layout()
    out = os.path.join(CHARTS_DIR, "seasonal_aqi_comparison.png")
    plt.savefig(out)
    plt.close()
    print(f"Generated: {out}")

def chart_3_monthly_trend():
    df = pd.read_csv("results/7_month_trends.csv")
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.plot(month_names, df['avg_aqi'], marker='o', linewidth=2.8, color='#DC2626', markersize=8)
    
    for i, txt in enumerate(df['avg_aqi']):
        ax.annotate(f"{txt:.1f}", (month_names[i], df['avg_aqi'][i] + 4), ha='center', fontsize=9, weight='bold')

    ax.set_ylabel("Average AQI Value", fontsize=12, weight='bold')
    ax.set_xlabel("Month", fontsize=12, weight='bold')
    ax.set_title("Monthly Seasonality Progression (2015 - 2023 Mean)", fontsize=14, weight='bold', pad=15)
    ax.set_ylim(50, 200)
    plt.tight_layout()
    out = os.path.join(CHARTS_DIR, "monthly_seasonality_trend.png")
    plt.savefig(out)
    plt.close()
    print(f"Generated: {out}")

def chart_4_annual_timeline():
    df = pd.read_csv("results/6_year_average_aqi.csv")
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    
    ax.plot(df['record_year'].astype(str), df['avg_aqi'], marker='s', linewidth=2.8, color='#2563EB', markersize=8)
    for i, txt in enumerate(df['avg_aqi']):
        ax.annotate(f"{txt:.1f}", (str(df['record_year'][i]), df['avg_aqi'][i] + 3), ha='center', fontsize=10, weight='bold')

    ax.axhspan(0, 50, color='#22C55E', alpha=0.15, label='Good (0-50)')
    ax.axhspan(51, 100, color='#84CC16', alpha=0.15, label='Satisfactory (51-100)')
    ax.axhspan(101, 200, color='#EAB308', alpha=0.15, label='Moderate (101-200)')

    ax.set_ylabel("Annual Average AQI", fontsize=12, weight='bold')
    ax.set_xlabel("Calendar Year", fontsize=12, weight='bold')
    ax.set_title("Annual Air Quality Index Progression (2015 - 2023)", fontsize=14, weight='bold', pad=15)
    ax.set_ylim(50, 180)
    ax.legend(loc='lower left', frameon=True)
    plt.tight_layout()
    out = os.path.join(CHARTS_DIR, "annual_aqi_timeline.png")
    plt.savefig(out)
    plt.close()
    print(f"Generated: {out}")

def chart_5_top_polluted_cities():
    df = pd.read_csv("results/12_top_polluted_cities.csv").head(12)
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    
    y_pos = range(len(df))
    bars = ax.barh(y_pos, df['avg_aqi'], color='#EA580C', height=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df['city'])
    ax.invert_yaxis()
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 3, bar.get_y() + bar.get_height()/2, f"{width:.1f}", ha='left', va='center', weight='bold', fontsize=9)

    ax.set_xlabel("Average AQI Value", fontsize=12, weight='bold')
    ax.set_title("Top 12 Most Polluted Cities in India (>= 100 Observations)", fontsize=14, weight='bold', pad=15)
    ax.set_xlim(0, 280)
    plt.tight_layout()
    out = os.path.join(CHARTS_DIR, "top_polluted_cities.png")
    plt.savefig(out)
    plt.close()
    print(f"Generated: {out}")

def chart_6_pollutant_frequency():
    df = pd.read_csv("results/10_pollutant_frequency.csv").head(7)
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    
    bars = ax.bar(df['individual_pollutant'], df['reporting_frequency'], color='#0D9488', width=0.55)
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 2000, f"{yval:,}", ha='center', va='bottom', weight='bold', fontsize=9)

    ax.set_ylabel("Reporting Frequency in Bulletins", fontsize=12, weight='bold')
    ax.set_xlabel("Prominent Pollutant Chemical Type", fontsize=12, weight='bold')
    ax.set_title("Prominent Pollutant Reporting Frequency (Hive Lateral View Explode)", fontsize=14, weight='bold', pad=15)
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
    ax.set_ylim(0, 180000)
    plt.tight_layout()
    out = os.path.join(CHARTS_DIR, "dominant_pollutants_frequency.png")
    plt.savefig(out)
    plt.close()
    print(f"Generated: {out}")

def chart_7_yoy_growth():
    df = pd.read_csv("results/14_yoy_changes.csv").dropna(subset=['pct_change'])
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    
    colors = ['#EF4444' if x > 0 else '#10B981' for x in df['pct_change']]
    bars = ax.bar(df['record_year'].astype(str), df['pct_change'], color=colors, width=0.5)
    
    for bar in bars:
        h = bar.get_height()
        va = 'bottom' if h >= 0 else 'top'
        ypos = h + 0.3 if h >= 0 else h - 0.7
        ax.text(bar.get_x() + bar.get_width()/2.0, ypos, f"{h:+.2f}%", ha='center', va=va, weight='bold', fontsize=10)

    ax.axhline(0, color='black', linewidth=1)
    ax.set_ylabel("% Change in Mean AQI vs Previous Year", fontsize=12, weight='bold')
    ax.set_xlabel("Calendar Year", fontsize=12, weight='bold')
    ax.set_title("Year-over-Year (YoY) AQI Dynamics (Hive SQL Window Functions)", fontsize=14, weight='bold', pad=15)
    ax.set_ylim(-16, 5)
    plt.tight_layout()
    out = os.path.join(CHARTS_DIR, "yoy_aqi_growth.png")
    plt.savefig(out)
    plt.close()
    print(f"Generated: {out}")

if __name__ == "__main__":
    print("Generating High-Resolution Visualization Charts...")
    chart_1_category_distribution()
    chart_2_seasonal_aqi()
    chart_3_monthly_trend()
    chart_4_annual_timeline()
    chart_5_top_polluted_cities()
    chart_6_pollutant_frequency()
    chart_7_yoy_growth()
    print("All charts successfully generated!")
