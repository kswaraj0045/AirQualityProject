"""
scripts/run_hive_analysis.py
Executes Hive DDL, population, and 14 analytical queries via Beeline inside Docker.
Exports formatted outputs and CSV results for the Streamlit dashboard.
"""

import os
import subprocess
import pandas as pd
import io
import re

HIVE_SERVER = "hive-server"
BEELINE_CMD = ["docker", "exec", "-i", HIVE_SERVER, "/opt/hive/bin/beeline", "-u", "jdbc:hive2://localhost:10000/air_quality_db", "-n", "root", "--silent=true", "--outputformat=csv2"]
BEELINE_PRETTY = ["docker", "exec", "-i", HIVE_SERVER, "/opt/hive/bin/beeline", "-u", "jdbc:hive2://localhost:10000/air_quality_db", "-n", "root"]

RESULTS_DIR = "results"
REPORTS_DIR = "results/reports"

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

def execute_hql_file(file_path, description):
    print(f"\n--> {description} ({file_path})...")
    with open(file_path, "r", encoding="utf-8") as f:
        hql_content = f.read()
    
    # Execute through docker exec stdin
    cmd = ["docker", "exec", "-i", HIVE_SERVER, "/opt/hive/bin/beeline", "-u", "jdbc:hive2://localhost:10000", "-n", "root"]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate(hql_content)
    
    if proc.returncode != 0:
        print(f"Warning/Error ({proc.returncode}):\n{stderr}")
    else:
        print("Completed successfully.")
    return stdout, stderr

def run_query(query, name, export_csv=True):
    print(f"Running Query: {name}...")
    cmd = BEELINE_CMD + ["-e", query]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate()
    
    if proc.returncode != 0:
        print(f"Error running {name}:\n{stderr}")
        return None
    
    # Clean output lines
    lines = [line.strip() for line in stdout.strip().split("\n") if line.strip() and not line.startswith("SLF4J") and not line.startswith("Connecting") and not line.startswith("Connected") and not line.startswith("Closing")]
    csv_text = "\n".join(lines)
    
    if export_csv and csv_text:
        out_path = os.path.join(RESULTS_DIR, f"{name}.csv")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(csv_text)
        print(f"  -> Exported: {out_path}")
        
    return csv_text

def run_pipeline():
    print("=" * 60)
    print("STARTING HIVE EXECUTION & ANALYTICAL PIPELINE")
    print("=" * 60)

    # 1. Create Database
    execute_hql_file("hive/create_database.hql", "Creating Database")

    # 2. Create Tables & Ingest into Managed ORC
    execute_hql_file("hive/create_tables.hql", "Creating Staging & ORC Tables")

    # 3. Execute 14 Analytical Queries
    queries = {
        "1_total_records": "SELECT COUNT(*) AS total_records FROM air_quality_records;",
        "2_total_cities": "SELECT COUNT(DISTINCT city) AS total_cities FROM air_quality_records;",
        "3_overall_statistics": "SELECT MIN(index_value) AS min_aqi, MAX(index_value) AS max_aqi, ROUND(AVG(index_value), 2) AS avg_aqi, ROUND(STDDEV_POP(index_value), 2) AS stddev_aqi FROM air_quality_records;",
        "4_city_average_aqi": "SELECT city, ROUND(AVG(index_value), 2) AS avg_aqi, COUNT(*) AS records FROM air_quality_records GROUP BY city ORDER BY avg_aqi DESC;",
        "5_city_max_aqi": "SELECT city, MAX(index_value) AS max_aqi, COUNT(*) AS records FROM air_quality_records GROUP BY city ORDER BY max_aqi DESC;",
        "6_year_average_aqi": "SELECT record_year, COUNT(*) AS total_records, ROUND(AVG(index_value), 2) AS avg_aqi, MIN(index_value) AS min_aqi, MAX(index_value) AS max_aqi FROM air_quality_records GROUP BY record_year ORDER BY record_year ASC;",
        "7_month_trends": "SELECT record_month, COUNT(*) AS observation_count, ROUND(AVG(index_value), 2) AS avg_aqi, ROUND(STDDEV_POP(index_value), 2) AS stddev_aqi FROM air_quality_records GROUP BY record_month ORDER BY record_month ASC;",
        "8_seasonal_aqi": "SELECT season, COUNT(*) AS total_records, ROUND(AVG(index_value), 2) AS avg_aqi, MIN(index_value) AS min_aqi, MAX(index_value) AS max_aqi FROM air_quality_records GROUP BY season ORDER BY avg_aqi DESC;",
        "9_category_distribution": "SELECT air_quality, COUNT(*) AS category_count, ROUND(COUNT(*) * 100.0 / 299974, 2) AS percentage FROM air_quality_records GROUP BY air_quality ORDER BY category_count DESC;",
        "10_pollutant_frequency": "SELECT individual_pollutant, COUNT(*) AS reporting_frequency, ROUND(COUNT(*) * 100.0 / 349147, 2) AS frequency_percentage FROM v_individual_pollutants GROUP BY individual_pollutant ORDER BY reporting_frequency DESC;",
        "11_city_pollutant_frequency": "SELECT city, individual_pollutant, COUNT(*) AS report_count FROM v_individual_pollutants WHERE city IN ('Delhi', 'Varanasi', 'Kanpur', 'Mumbai', 'Kolkata', 'Bengaluru', 'Hyderabad', 'Chennai') GROUP BY city, individual_pollutant ORDER BY city, report_count DESC;",
        "12_top_polluted_cities": "SELECT city, ROUND(AVG(index_value), 2) AS avg_aqi, COUNT(*) AS observations FROM air_quality_records GROUP BY city HAVING COUNT(*) >= 100 ORDER BY avg_aqi DESC LIMIT 20;",
        "13_highest_lowest_periods": "SELECT concat(record_year, '-', lpad(record_month, 2, '0')) AS period_ym, ROUND(AVG(index_value), 2) AS avg_aqi, COUNT(*) AS observations FROM air_quality_records GROUP BY record_year, record_month ORDER BY avg_aqi DESC;",
        "14_yoy_changes": "WITH yearly AS (SELECT record_year, ROUND(AVG(index_value), 2) AS avg_aqi FROM air_quality_records GROUP BY record_year) SELECT record_year, avg_aqi, LAG(avg_aqi, 1) OVER (ORDER BY record_year) AS prev_year_aqi, ROUND(avg_aqi - LAG(avg_aqi, 1) OVER (ORDER BY record_year), 2) AS aqi_change, ROUND((avg_aqi - LAG(avg_aqi, 1) OVER (ORDER BY record_year)) * 100.0 / LAG(avg_aqi, 1) OVER (ORDER BY record_year), 2) AS pct_change FROM yearly ORDER BY record_year ASC;"
    }

    report_output = []
    report_output.append("# Hive Analysis Execution Report")
    report_output.append(f"Database: air_quality_db\nExecution Engine: Apache Hive on Hadoop HDFS\n")

    for name, q in queries.items():
        csv_res = run_query(q, name)
        report_output.append(f"## {name.replace('_', ' ').title()}")
        report_output.append(f"```sql\n{q}\n```")
        report_output.append(f"```csv\n{csv_res}\n```\n")

    # Save aggregated report
    report_path = os.path.join(REPORTS_DIR, "hive_analysis_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_output))
    print(f"\nAggregated Hive Analysis Report saved: {report_path}")

    print("=" * 60)
    print("HIVE PIPELINE & ANALYTICAL EXECUTION COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()
