# Spatio-Temporal Air Quality and Dominant Pollutant Analysis Using Hadoop and Hive

[![Hadoop](https://img.shields.io/badge/Apache%20Hadoop-3.2.1-FFD000?style=flat&logo=apachehadoop&logoColor=black)](https://hadoop.apache.org/)
[![Hive](https://img.shields.io/badge/Apache%20Hive-2.3.2-FDEE21?style=flat&logo=apachehive&logoColor=black)](https://hive.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-Desktop-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)

A complete enterprise-grade Big Data Engineering pipeline implementing distributed storage, columnar analytical processing, and interactive web visualization for **299,974 daily bulletin records** across **277 Indian cities** from **2015 to 2023**.

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [Problem Statement](#2-problem-statement)
3. [Objectives](#3-objectives)
4. [Technologies Used](#4-technologies-used)
5. [System Architecture](#5-system-architecture)
6. [Dataset Description](#6-dataset-description)
7. [Data Preprocessing Pipeline](#7-data-preprocessing-pipeline)
8. [Hadoop / HDFS Implementation](#8-hadoophdfs-implementation)
9. [Hive Warehouse Implementation](#9-hive-warehouse-implementation)
10. [Analysis Results (14 Core Queries)](#10-analysis-results-14-core-queries)
11. [Streamlit Dashboard](#11-streamlit-dashboard)
12. [Step-by-Step Execution Guide](#12-step-by-step-execution-guide)
13. [Testing & Verification](#13-testing--verification)
14. [Limitations & Ethical Considerations](#14-limitations--ethical-considerations)

---

## 1. Introduction

Ambient air pollution in India is one of the most pressing environmental health challenges of the 21st century. The Central Pollution Control Board (CPCB) publishes daily Air Quality Index (AQI) bulletins classifying municipal air quality and designating the prominent pollutant responsible for the index value. 

This project establishes an automated, production-grade Big Data pipeline to ingest, preprocess, store, and analyze nine years of daily CPCB bulletin data (2015–2023) using a containerized ecosystem of **Apache Hadoop HDFS**, **Apache Hive with PostgreSQL Metastore**, and an interactive **Streamlit/Plotly** dashboard.

---

## 2. Problem Statement

Historical CPCB air quality bulletins present several big data and engineering challenges:
- **Massive Longitudinal Scale:** 299,974 records across 277 cities over 9 years require distributed, fault-tolerant storage and scalable SQL query engines.
- **Semi-Structured Multi-Pollutant Text:** Many bulletins designate compound pollutants (e.g., `"PM10, PM2.5"` or `"CO, O3, PM10"`), making direct relational filtering inaccurate without decomposition.
- **OCR Formatting Artifacts:** Real-world government bulletin digitization introduced typographical artifacts in station count metrics (e.g., `"1 (@ 2.00 PM)"`, `"2!"`, `"(1"`).
- **Domain Reporting Restrictions:** Bulletins designate *prominent pollutants* rather than individual numerical pollutant concentrations. Analyses must respect this boundary and avoid fabricating synthetic concentrations.

---

## 3. Objectives

- **Fault-Tolerant Infrastructure:** Deploy a containerized cluster of Hadoop NameNode, DataNode, Hive Metastore, HiveServer2, and PostgreSQL catalog via Docker Compose.
- **Transparent Data Cleansing:** Build an automated Python ETL pipeline that normalizes dates, remedies OCR artifacts, standardizes chemical nomenclature (`OZONE` $\rightarrow$ `O3`), and adds derived temporal partitions without modifying original data.
- **Distributed Ingestion:** Ingest cleaned data into Hadoop HDFS under a structured namespace (`/airquality/input`, `/airquality/processed`, `/airquality/output`).
- **High-Performance Warehousing:** Design external staging tables (`OpenCSVSerde`) and managed columnar ORC tables (`Snappy` compression), with lateral view exploded arrays for multi-pollutant decomposition.
- **Analytical Execution:** Execute 14 analytical HiveQL queries covering overall statistics, municipal rankings, monthly seasonality, annual timelines, CPCB category breakdowns, and year-over-year growth (`LAG()`).
- **Executive Visualization:** Build a professional Streamlit web dashboard directly backed by verified Hive query outputs.

---

## 4. Technologies Used

| Tier | Component | Version | Role in Project |
| :--- | :--- | :--- | :--- |
| **Distributed Storage** | Apache Hadoop HDFS | 3.2.1 | Fault-tolerant distributed block storage across NameNode and DataNode |
| **Data Warehousing** | Apache Hive | 2.3.2 | Distributed SQL queries, managed ORC tables, Snappy compression |
| **Metastore Catalog** | PostgreSQL | 15.0 | Relational relational catalog store maintaining schema and table metadata |
| **Containerization** | Docker Desktop & Compose | 29.7 / v5.4 | Microservice container orchestration over isolated bridge network (`bda_network`) |
| **Data Engineering** | Python & Pandas | 3.10 / 2.3.3 | Automated data cleansing, OCR artifact remediation, and test orchestration |
| **Interactive Dashboard**| Streamlit & Plotly | 1.35 / 5.22 | Web dashboard with dynamic filtering, KPI cards, and interactive charts |

---

## 5. System Architecture

```text
+-----------------------------------------------------------------------------------+
|                              DATA PIPELINE ARCHITECTURE                           |
+-----------------------------------------------------------------------------------+
|  Original Raw Dataset: India_AQI_Bulletins_Master.csv (299,974 records, 11.6 MB)  |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                 ETL Preprocessing Pipeline (scripts/clean_dataset.py)              |
|  - ISO Date Normalization (YYYY-MM-DD)    - Station Count OCR Remediation         |
|  - Chemical Formula Standardization (O3)  - IMD Season & Year/Month Derived Feats |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|          Cleaned Warehouse Dataset: dataset/processed/air_quality_cleaned.csv     |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                       Apache Hadoop Distributed File System (HDFS)                |
|  - /airquality/input/air_quality_cleaned.csv (16.4 MB, 299,975 lines)            |
|  - /airquality/processed/  |  /airquality/output/  |  /airquality/database/       |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                            Apache Hive Data Warehouse                             |
|  - air_quality_db.air_quality_raw (External Table via OpenCSVSerde)               |
|  - air_quality_db.air_quality_records (Managed Table, Stored as ORC, Snappy)     |
|  - air_quality_db.v_individual_pollutants (LATERAL VIEW explode(split(...)))      |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                         14 Analytical HiveQL Query Executions                     |
|  - Overall Stats | City AQI | Year Avg | Monthly Cycles | Seasonal | YoY LAG()    |
|  - Prominent Pollutant Reporting Frequencies | Metropolitan Matrix Breakdown      |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                       Interactive Streamlit Analytics Dashboard                   |
|  - Executive Overview | Temporal Trends | City Analysis | Pollutant Dynamics      |
|  - Multi-parameter dynamic filtering & Hive SQL Code Catalog                      |
+-----------------------------------------------------------------------------------+
```

---

## 6. Dataset Description

- **Source:** Central Pollution Control Board (CPCB), Ministry of Environment, Forest and Climate Change, Government of India.
- **Records:** Exactly 299,974 daily bulletin observations.
- **Temporal Span:** May 1, 2015 to December 31, 2023 (9 full years).
- **Spatial Coverage:** 277 distinct cities across all Indian States and Union Territories.
- **Schema Attributes:**
  - `date`: Daily observation date (parsed to `YYYY-MM-DD`).
  - `city`: Monitored municipal center (Title Case).
  - `no_stations`: Active monitoring stations (cleaned nullable integer).
  - `air_quality`: CPCB health category (`Good`, `Satisfactory`, `Moderate`, `Poor`, `Very Poor`, `Severe`).
  - `index_value`: National Air Quality Index (integer [3, 500]).
  - `prominent_pollutant`: Designated dominant pollutant (`PM10`, `PM2.5`, `O3`, `CO`, `NO2`, `SO2`, `NH3`, or multi-pollutant combinations).
  - `year`, `month`, `season`: Derived temporal dimensions.

---

## 7. Data Preprocessing Pipeline

Run via `python scripts/clean_dataset.py`:
1. **Deduplication:** Confirmed 0 duplicate rows.
2. **Date Parsing:** Standardized all dates to ISO `YYYY-MM-DD` without any drops.
3. **Station OCR Remediation:** Extracted numeric counts using regex `r'\d+'` from OCR artifacts (e.g., `1 (@ 2.00 PM)` $\rightarrow$ `1`), preserving genuine nulls.
4. **Category Normalization:** Resolved casing inconsistencies (`Very poor` $\rightarrow$ `Very Poor`).
5. **Chemical Standardization:** Mapped `OZONE` $\rightarrow$ `O3`, and normalized multi-pollutants to comma-space separated strings.
6. **Temporal Partition Columns:** Added `year` (2015–2023), `month` (1–12), and `season` (Winter, Summer, Monsoon, Post-Monsoon).

---

## 8. Hadoop / HDFS Implementation

The cluster runs in Docker with persistent volumes:
- NameNode: `bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8` (Ports 9870, 9000)
- DataNode: `bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8` (Port 9864)

Ingestion is automated via `scripts/upload_to_hdfs.py`:
```bash
docker exec namenode hdfs dfs -mkdir -p /airquality/input
docker exec namenode hdfs dfs -mkdir -p /airquality/processed
docker exec namenode hdfs dfs -mkdir -p /airquality/output
docker exec namenode hdfs dfs -put -f /tmp/air_quality_cleaned.csv /airquality/input/air_quality_cleaned.csv
```

**Verification:**
- File size in HDFS: `17,190,284 bytes` (16.4 MB)
- Line count in HDFS: `299,975 lines` (1 header + 299,974 records)
- Cluster health: 1 Live DataNode, 937.43 GB free DFS capacity, 0 corrupted/missing blocks.

---

## 9. Hive Warehouse Implementation

### 9.1 Database & Staging Table
Defined in `hive/create_tables.hql`:
```sql
CREATE DATABASE IF NOT EXISTS air_quality_db LOCATION '/airquality/database/';
USE air_quality_db;

CREATE EXTERNAL TABLE IF NOT EXISTS air_quality_raw (
    record_date STRING, city STRING, no_stations STRING, air_quality STRING,
    index_value STRING, prominent_pollutant STRING, record_year STRING,
    record_month STRING, season STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ("separatorChar" = ",", "quoteChar" = "\"", "escapeChar" = "\\")
LOCATION '/airquality/input/'
TBLPROPERTIES ("skip.header.line.count"="1");
```

### 9.2 Production Managed ORC Table
```sql
CREATE TABLE IF NOT EXISTS air_quality_records (
    record_date DATE, city STRING, no_stations INT, air_quality STRING,
    index_value INT, prominent_pollutant STRING, record_year INT,
    record_month INT, season STRING
)
STORED AS ORC
TBLPROPERTIES ("orc.compress"="SNAPPY");

INSERT OVERWRITE TABLE air_quality_records
SELECT CAST(record_date AS DATE), trim(city), CAST(no_stations AS INT),
       trim(air_quality), CAST(index_value AS INT), trim(prominent_pollutant),
       CAST(record_year AS INT), CAST(record_month AS INT), trim(season)
FROM air_quality_raw
WHERE record_date != 'date' AND index_value IS NOT NULL;
```

### 9.3 Multi-Pollutant Exploded View
```sql
CREATE OR REPLACE VIEW v_individual_pollutants AS
SELECT record_date, city, index_value, air_quality, record_year, record_month, season,
       trim(single_pollutant) AS individual_pollutant
FROM air_quality_records
LATERAL VIEW explode(split(prominent_pollutant, ',\\s*')) t AS single_pollutant
WHERE trim(single_pollutant) != '' AND trim(single_pollutant) != 'UNKNOWN';
```

---

## 10. Analysis Results (14 Core Queries)

All queries are executed against Hive via Beeline and exported to `results/`:

| # | Analysis | SQL Logic | Output Key Finding |
| :--- | :--- | :--- | :--- |
| **1** | Total Records | `SELECT COUNT(*) FROM air_quality_records` | **299,974** records |
| **2** | Total Cities | `SELECT COUNT(DISTINCT city)` | **277** monitored cities |
| **3** | Overall Statistics | `SELECT MIN, MAX, AVG, STDDEV_POP` | Min: **3**, Max: **500**, Avg: **124.69**, StdDev: **85.09** |
| **4** | City Average AQI | `GROUP BY city ORDER BY avg_aqi DESC` | Byrnihat: **248.67**, Begusarai: **248.14**, Ghaziabad: **221.64** |
| **5** | City Maximum AQI | `SELECT city, MAX(index_value)` | 32 cities recorded maximum hazardous ceiling of **500** |
| **6** | Year-wise Trends | `GROUP BY record_year ORDER BY record_year` | 2015: **156.54** $\rightarrow$ 2019: **136.32** $\rightarrow$ 2023: **121.36** |
| **7** | Month-wise Seasonality | `GROUP BY record_month ORDER BY record_month` | January peak (**175.22**) $\rightarrow$ Monsoon trough in July (**72.84**) |
| **8** | Seasonal Analysis | `GROUP BY season ORDER BY avg_aqi DESC` | Winter: **169.25** \| Post-Monsoon: **154.11** \| Summer: **123.05** \| Monsoon: **76.98** |
| **9** | Category Distribution | `GROUP BY air_quality ORDER BY count DESC` | Satisfactory: **35.1%**, Moderate: **32.1%**, Good: **15.8%**, Poor: **11.6%**, Very Poor: **4.7%**, Severe: **0.8%** |
| **10** | Prominent Pollutants | `SELECT individual_pollutant, COUNT(*)` | PM10: **43.68%** (152,517), PM2.5: **32.31%** (112,808), O3: **9.24%** (32,263), CO: **7.78%** (27,160) |
| **11** | City Pollutant Matrix | Filtered metropolitan matrix | Bengaluru: PM10 (2,136), PM2.5 (2,033), CO (1,304), O3 (924) |
| **12** | Top Polluted Cities | `HAVING COUNT(*) >= 100 ORDER BY avg_aqi DESC` | Byrnihat (**248.67**), Begusarai (**248.14**), Ghaziabad (**221.64**), Delhi (**217.14**) |
| **13** | Extreme Periods | `GROUP BY year, month ORDER BY avg_aqi` | Peak: Jan 2016 (**252.18**) \| Cleanest: Aug 2020 (**61.96**) |
| **14** | YoY Growth (`LAG`) | `ROUND((avg - LAG(avg)) * 100 / LAG(avg), 2)` | 2016: **+0.33%** \| 2017: **-3.26%** \| 2018: **-3.38%** \| 2019: **-7.13%** \| 2020: **-12.87%** |

---

## 11. Streamlit Dashboard

Launch the dashboard locally:
```bash
streamlit run dashboard/app.py
```
Access at: `http://localhost:8501`

**Features:**
- **Executive Overview:** 5 live KPI metric cards, interactive CPCB tier donut chart, and 2015–2023 historical timeline.
- **Temporal Analysis:** Monthly cycle line chart and interactive YoY percentage growth chart.
- **City Analysis:** Horizontal rankings of most polluted cities, maximum AQI table, and monthly extreme periods.
- **Dominant Pollutant Dynamics:** Breakdown of particulate vs gaseous prominent pollutants, and grouped metropolitan matrix.
- **Data Explorer & Hive Catalog:** Interactive data table with direct CSV slice download and expandable HiveQL code viewer.

---

## 12. Step-by-Step Execution Guide

### 1. Prerequisites
- Docker Desktop running with at least 5 GB free disk space.
- Python 3.10 installed with required packages:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Run Data Preprocessing
```bash
python scripts/clean_dataset.py
python -m unittest tests/test_preprocessing.py
```

### 3. Start Hadoop and Hive Cluster
```bash
cd hadoop-hive
docker compose up -d
cd ..
```

### 4. Ingest Cleaned Data into HDFS
```bash
python scripts/upload_to_hdfs.py
```

### 5. Execute Hive DDL & Analytical Queries
```bash
python scripts/run_hive_analysis.py
```

### 6. Generate High-Resolution Charts & Word Report
```bash
python scripts/generate_charts.py
python scripts/generate_word_report.py
```

### 7. Run Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```

### 8. Run End-to-End Regression Suite
```bash
python -m unittest tests/test_end_to_end.py
```

---

## 13. Testing & Verification

The project includes unit and integration test suites:
- [tests/test_preprocessing.py](file:///c:/Users/LENOVO/Desktop/BDA/tests/test_preprocessing.py): Validates 9 data quality rules (0 nulls in critical fields, ISO dates, integer AQI in [0, 500], CPCB category normalization).
- [tests/test_end_to_end.py](file:///c:/Users/LENOVO/Desktop/BDA/tests/test_end_to_end.py): Validates all 6 architectural pipeline tiers (raw/clean CSVs, HDFS file existence, Hive ORC tables and views, 299,974 record count match, 14 exported CSV files, dashboard file integrity).

```text
Ran 6 tests in 4.470s
OK
```

---

## 14. Limitations & Ethical Considerations

1. **Prominent Pollutant vs Concentration:** The CPCB bulletins record the dominant pollutant responsible for the overall index value on a given day. The data does *not* contain continuous micrograms per cubic meter ($\mu g/m^3$) mass concentrations for individual pollutants. Describing pollutant counts as concentrations is scientifically invalid; our metrics report *reporting frequency*.
2. **Monitoring Station Densities:** Larger metropolitan centers (such as Delhi with up to 39 active stations) have denser spatial sampling than smaller tier-3 municipal centers with single stations.
3. **Absence of Geographical Coordinates:** The raw bulletin dataset does not contain geographical latitude and longitude coordinates. Spatial visualizations rely strictly on municipal administrative boundaries.
