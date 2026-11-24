"""
scripts/inspect_dataset.py
Performs exploratory data inspection on the raw air quality dataset.
"""

import os
import pandas as pd
import numpy as np

def inspect(file_path):
    print("=" * 60)
    print(f"INSPECTING DATASET: {file_path}")
    print("=" * 60)

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Read dataset
    df = pd.read_csv(file_path, low_memory=False)

    print(f"\n1. Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
    print("\n2. Columns & Data Types:")
    for col, dtype in df.dtypes.items():
        print(f"   - {col}: {dtype}")

    print("\n3. Missing Value Analysis:")
    null_counts = df.isnull().sum()
    for col in df.columns:
        cnt = null_counts[col]
        pct = (cnt / len(df)) * 100
        print(f"   - {col}: {cnt:,} missing ({pct:.2f}%)")

    print(f"\n4. Duplicate Rows: {df.duplicated().sum():,}")

    # Inspect Date
    print("\n5. Date Column Analysis:")
    try:
        parsed_dates = pd.to_datetime(df['date'], errors='coerce')
        invalid_dates = parsed_dates.isnull().sum()
        print(f"   - Invalid date entries: {invalid_dates}")
        print(f"   - Min Date: {parsed_dates.min().strftime('%Y-%m-%d')}")
        print(f"   - Max Date: {parsed_dates.max().strftime('%Y-%m-%d')}")
        print(f"   - Years covered: {sorted(parsed_dates.dt.year.dropna().unique().astype(int).tolist())}")
    except Exception as e:
        print(f"   - Date parsing error: {e}")

    # Inspect City
    print("\n6. City Analysis:")
    cities = df['City'].dropna().astype(str).str.strip()
    print(f"   - Unique raw cities: {cities.nunique():,}")
    print(f"   - Sample cities (first 10): {cities.unique()[:10].tolist()}")

    # Inspect Index Value (AQI)
    print("\n7. Index Value (AQI) Analysis:")
    numeric_aqi = pd.to_numeric(df['Index Value'], errors='coerce')
    non_numeric_aqi = df['Index Value'].notnull() & numeric_aqi.isnull()
    print(f"   - Valid numeric AQI count: {numeric_aqi.notnull().sum():,}")
    print(f"   - Non-numeric AQI values count: {non_numeric_aqi.sum():,}")
    if non_numeric_aqi.sum() > 0:
        print(f"   - Sample non-numeric values: {df.loc[non_numeric_aqi, 'Index Value'].unique()[:5].tolist()}")
    print(f"   - AQI Min: {numeric_aqi.min()}")
    print(f"   - AQI Max: {numeric_aqi.max()}")
    print(f"   - AQI Mean: {numeric_aqi.mean():.2f}")
    print(f"   - AQI Median: {numeric_aqi.median():.2f}")

    # Inspect Air Quality Category
    print("\n8. Air Quality Categories:")
    print(df['Air Quality'].value_counts(dropna=False).to_string())

    # Inspect Prominent Pollutant
    print("\n9. Prominent Pollutant Distribution (Top 15):")
    print(df['Prominent Pollutant'].value_counts(dropna=False).head(15).to_string())

    # Inspect No. Stations
    print("\n10. No. Stations Summary:")
    stations_num = pd.to_numeric(df['No. Stations'], errors='coerce')
    print(f"   - Valid numeric counts: {stations_num.notnull().sum():,}")
    print(f"   - Missing/invalid counts: {stations_num.isnull().sum():,}")
    print(f"   - Min stations: {stations_num.min()}, Max stations: {stations_num.max()}")

    print("\n" + "=" * 60)
    print("INSPECTION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    inspect("dataset/raw/India_AQI_Bulletins_Master.csv")
