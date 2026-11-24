"""
tests/test_end_to_end.py
Comprehensive End-to-End Test Suite for the Big Data Pipeline.
Validates:
1. Raw and Cleaned Dataset Integrity
2. HDFS Directory Hierarchy and Storage
3. Hive Tables, Schema, and Record Counts
4. Exported Analysis Datasets (14 Queries)
5. Dashboard Prerequisites
"""

import os
import unittest
import subprocess
import pandas as pd

class TestBigDataPipelineE2E(unittest.TestCase):

    def test_01_raw_and_cleaned_datasets_exist(self):
        """Verify raw and processed datasets exist and have expected sizes."""
        raw_path = "dataset/raw/India_AQI_Bulletins_Master.csv"
        cleaned_path = "dataset/processed/air_quality_cleaned.csv"
        
        self.assertTrue(os.path.exists(raw_path), "Raw dataset missing in dataset/raw/")
        self.assertTrue(os.path.exists(cleaned_path), "Cleaned dataset missing in dataset/processed/")
        
        # Verify row counts
        df_clean = pd.read_csv(cleaned_path, nrows=10)
        self.assertEqual(len(df_clean.columns), 9, "Cleaned dataset should have 9 columns.")

    def test_02_hdfs_directory_structure(self):
        """Verify HDFS directories and files exist inside Hadoop cluster."""
        cmd = ["docker", "exec", "namenode", "hdfs", "dfs", "-test", "-e", "/airquality/input/air_quality_cleaned.csv"]
        res = subprocess.run(cmd, capture_output=True)
        self.assertEqual(res.returncode, 0, "Cleaned dataset not found in HDFS /airquality/input/")

    def test_03_hive_tables_and_view(self):
        """Verify Hive database, managed ORC table, and exploded view."""
        cmd = [
            "docker", "exec", "hive-server", 
            "/opt/hive/bin/beeline", 
            "-u", "jdbc:hive2://localhost:10000/air_quality_db", 
            "-n", "root", 
            "--silent=true", 
            "-e", "SHOW TABLES;"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Failed to query Hive tables: {res.stderr}")
        self.assertIn("air_quality_records", res.stdout, "ORC table air_quality_records missing from Hive.")
        self.assertIn("v_individual_pollutants", res.stdout, "Exploded view missing from Hive.")

    def test_04_hive_record_count(self):
        """Verify Hive ORC table contains all 299,974 records."""
        count_file = "results/1_total_records.csv"
        self.assertTrue(os.path.exists(count_file), "Total records result CSV missing.")
        df = pd.read_csv(count_file)
        total = int(df.iloc[0, 0])
        self.assertEqual(total, 299974, f"Expected 299,974 records in Hive table, got {total}")

    def test_05_exported_analytical_datasets(self):
        """Verify all 14 analysis query outputs were exported to results/."""
        expected_files = [
            "1_total_records.csv",
            "2_total_cities.csv",
            "3_overall_statistics.csv",
            "4_city_average_aqi.csv",
            "5_city_max_aqi.csv",
            "6_year_average_aqi.csv",
            "7_month_trends.csv",
            "8_seasonal_aqi.csv",
            "9_category_distribution.csv",
            "10_pollutant_frequency.csv",
            "11_city_pollutant_frequency.csv",
            "12_top_polluted_cities.csv",
            "13_highest_lowest_periods.csv",
            "14_yoy_changes.csv"
        ]
        for ef in expected_files:
            fp = os.path.join("results", ef)
            self.assertTrue(os.path.exists(fp), f"Missing exported analysis file: {ef}")
            self.assertGreater(os.path.getsize(fp), 0, f"Exported file is empty: {ef}")

    def test_06_dashboard_script_exists(self):
        """Verify Streamlit app script exists."""
        self.assertTrue(os.path.exists("dashboard/app.py"), "dashboard/app.py is missing.")

if __name__ == "__main__":
    unittest.main()
