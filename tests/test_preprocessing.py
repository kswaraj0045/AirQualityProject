"""
tests/test_preprocessing.py
Unit tests and validation checks for dataset preprocessing.
"""

import os
import unittest
import pandas as pd

CLEANED_CSV = "dataset/processed/air_quality_cleaned.csv"
RAW_CSV = "dataset/raw/India_AQI_Bulletins_Master.csv"

class TestDatasetPreprocessing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(CLEANED_CSV):
            raise unittest.SkipTest(f"Processed file does not exist: {CLEANED_CSV}")
        cls.df = pd.read_csv(CLEANED_CSV, low_memory=False)

    def test_file_exists_and_non_empty(self):
        """Test cleaned CSV exists and is greater than 1MB."""
        self.assertTrue(os.path.exists(CLEANED_CSV), "Cleaned file not found.")
        self.assertGreater(os.path.getsize(CLEANED_CSV), 1_000_000, "File size suspiciously small.")

    def test_row_count(self):
        """Test row count is equal to the raw records."""
        raw_df = pd.read_csv(RAW_CSV, low_memory=False)
        self.assertEqual(len(self.df), len(raw_df), "Cleaned row count does not match raw row count.")

    def test_column_presence_and_order(self):
        """Test expected columns exist."""
        expected_cols = [
            "date", "city", "no_stations", "air_quality",
            "index_value", "prominent_pollutant", "year", "month", "season"
        ]
        self.assertListEqual(list(self.df.columns), expected_cols)

    def test_no_nulls_in_critical_columns(self):
        """Test critical columns have no null values."""
        critical_cols = ["date", "city", "air_quality", "index_value", "prominent_pollutant", "year", "month", "season"]
        for col in critical_cols:
            null_count = self.df[col].isnull().sum()
            self.assertEqual(null_count, 0, f"Critical column {col} has {null_count} nulls.")

    def test_date_format_and_range(self):
        """Test date conforms to YYYY-MM-DD and range is 2015-2023."""
        dates = pd.to_datetime(self.df['date'], format='%Y-%m-%d', errors='coerce')
        self.assertEqual(dates.isnull().sum(), 0, "Found invalid date formats.")
        self.assertEqual(dates.min().year, 2015)
        self.assertEqual(dates.max().year, 2023)

    def test_aqi_bounds(self):
        """Test AQI is numeric and strictly positive within valid CPCB range."""
        self.assertTrue(pd.api.types.is_numeric_dtype(self.df['index_value']))
        self.assertGreaterEqual(self.df['index_value'].min(), 0, "AQI below 0 found.")
        self.assertLessEqual(self.df['index_value'].max(), 500, "AQI above 500 found.")

    def test_air_quality_categories(self):
        """Test air quality categories match official standard CPCB categories."""
        expected_cats = {"Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"}
        actual_cats = set(self.df['air_quality'].unique())
        self.assertTrue(actual_cats.issubset(expected_cats), f"Unexpected air quality categories: {actual_cats - expected_cats}")

    def test_prominent_pollutant_normalized(self):
        """Test OZONE was replaced by O3 and no empty pollutants exist."""
        # Check no raw 'OZONE' word boundary remains
        ozone_matches = self.df[self.df['prominent_pollutant'].str.contains(r'\bOZONE\b', regex=True)]
        self.assertEqual(len(ozone_matches), 0, "OZONE was not properly converted to O3.")

    def test_derived_temporal_consistency(self):
        """Test year, month, and season match date."""
        dates = pd.to_datetime(self.df['date'])
        self.assertTrue((self.df['year'] == dates.dt.year).all(), "Year mismatch with date.")
        self.assertTrue((self.df['month'] == dates.dt.month).all(), "Month mismatch with date.")
        expected_seasons = {"Winter", "Summer", "Monsoon", "Post-Monsoon"}
        self.assertTrue(set(self.df['season'].unique()).issubset(expected_seasons))

if __name__ == "__main__":
    unittest.main()
