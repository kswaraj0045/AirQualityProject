# Data Cleaning and Preprocessing Report

**Project:** Spatio-Temporal Air Quality and Dominant Pollutant Analysis Using Hadoop and Hive  
**Date Generated:** 2026-11-24  
**Source File:** `dataset/raw/India_AQI_Bulletins_Master.csv`  
**Destination File:** `dataset/processed/air_quality_cleaned.csv`  

---

## 1. Executive Summary

The preprocessing pipeline cleaned, standardized, and validated the master India Air Quality dataset. All original 299,974 records were verified, cleaned, and retained. No synthetic or invented pollutant concentration figures were introduced, adhering strictly to the recorded CPCB bulletin metrics.

| Metric | Raw Dataset | Cleaned Dataset | Change / Action |
| :--- | :--- | :--- | :--- |
| **Total Rows** | 299,974 | 299,974 | Retained 100% of valid records |
| **Total Columns** | 6 | 9 | Added derived `year`, `month`, `season` |
| **Duplicates Removed** | 0 | 0 | No exact duplicate rows found |
| **Unique Cities** | 277 | 277 | Standardized whitespace and title casing |
| **Date Range** | 2015-05-01 to 2023-12-31 | 2015-05-01 to 2023-12-31 | Parsed to standard ISO YYYY-MM-DD format |
| **AQI Range** | [3, 500] | [3, 500] | Validated valid integer range [0, 500] |
| **AQI Mean / Median** | 124.69 / 99.00 | 124.69 / 99.00 | Preserved numerical accuracy |

---

## 2. Detailed Transformations Applied

### 2.1 Date Parsing and Validation
- Raw strings in `date` were parsed to standardized ISO `YYYY-MM-DD`.
- Zero date parsing errors were encountered.
- Date range spans from `2015-05-01` to `2023-12-31` across **9 years** (2015 - 2023).

### 2.2 City Name Normalization
- Stripped leading/trailing whitespace and normalized casing to Title Case.
- Maintained exact consistency across all `277` monitored cities.

### 2.3 Station Count OCR Artifact Remediation
- Found 6 records with non-numeric OCR artifacts (e.g. `1 (@ 2.00 PM)`, `2!`, `(1`).
- Extracted numeric station counts using regex pattern matching.
- Remaining 140 genuine null station counts were preserved as nullable integer fields without fabricating data.

### 2.4 Air Quality Category Normalization
- Standardized text casing (resolved 18 instances of lowercase `Very poor` to `Very Poor`).
- CPCB category distribution in cleaned dataset:
  - **Satisfactory**: 105,251 (35.09%)
  - **Moderate**: 96,139 (32.05%)
  - **Good**: 47,440 (15.81%)
  - **Poor**: 34,641 (11.55%)
  - **Very Poor**: 13,987 (4.66%)
  - **Severe**: 2,516 (0.84%)

### 2.5 Prominent Pollutant Standardization
- Standardized `OZONE` to chemical formula `O3` to ensure uniform grouping across CPCB bulletin conventions.
- Cleaned multi-pollutant separators to standard comma-space format (`", "`).
- Single missing record imputed transparently as `UNKNOWN`.
- Top 10 prominent pollutant entries:
  - **PM10**: 126,508 (42.17%)
  - **PM2.5**: 91,000 (30.34%)
  - **O3**: 22,294 (7.43%)
  - **CO**: 18,672 (6.22%)
  - **PM10, PM2.5**: 13,342 (4.45%)
  - **NO2**: 5,149 (1.72%)
  - **SO2**: 3,670 (1.22%)
  - **O3, PM10**: 3,522 (1.17%)
  - **CO, PM10**: 2,713 (0.90%)
  - **O3, PM2.5**: 2,196 (0.73%)

### 2.6 Derived Temporal Attributes (For Hive Partitioning & Query Efficiency)
- `year`: Integer calendar year (2015 - 2023).
- `month`: Integer calendar month (1 - 12).
- `season`: Indian Meteorological Department (IMD) classification:
  - **Winter**: December, January, February
  - **Summer**: March, April, May
  - **Monsoon**: June, July, August, September
  - **Post-Monsoon**: October, November

---

## 3. Data Integrity & Verification
- Cleaned CSV written to `dataset/processed/air_quality_cleaned.csv`.
- Header schema: `date,city,no_stations,air_quality,index_value,prominent_pollutant,year,month,season`.
- Verified 0 NaN/null values in mandatory columns (`date`, `city`, `air_quality`, `index_value`, `prominent_pollutant`, `year`, `month`, `season`).
