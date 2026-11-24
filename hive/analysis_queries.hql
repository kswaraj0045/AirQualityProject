-- hive/analysis_queries.hql
-- Comprehensive HiveQL Analytical Queries for Spatio-Temporal Air Quality Analysis

USE air_quality_db;

-- -------------------------------------------------------------
-- Query 1: Total Number of Records
-- -------------------------------------------------------------
SELECT COUNT(*) AS total_records 
FROM air_quality_records;

-- -------------------------------------------------------------
-- Query 2: Total Number of Unique Monitored Cities
-- -------------------------------------------------------------
SELECT COUNT(DISTINCT city) AS total_unique_cities 
FROM air_quality_records;

-- -------------------------------------------------------------
-- Query 3: Overall AQI Statistics (Min, Max, Avg, StdDev)
-- -------------------------------------------------------------
SELECT 
    MIN(index_value) AS min_aqi,
    MAX(index_value) AS max_aqi,
    ROUND(AVG(index_value), 2) AS avg_aqi,
    ROUND(STDDEV_POP(index_value), 2) AS stddev_aqi
FROM air_quality_records;

-- -------------------------------------------------------------
-- Query 4: City-wise Average AQI (Top 25)
-- -------------------------------------------------------------
SELECT 
    city,
    ROUND(AVG(index_value), 2) AS avg_aqi,
    COUNT(*) AS total_observations
FROM air_quality_records
GROUP BY city
ORDER BY avg_aqi DESC
LIMIT 25;

-- -------------------------------------------------------------
-- Query 5: City-wise Maximum AQI (Top 25)
-- -------------------------------------------------------------
SELECT 
    city,
    MAX(index_value) AS max_aqi,
    COUNT(*) AS total_observations
FROM air_quality_records
GROUP BY city
ORDER BY max_aqi DESC
LIMIT 25;

-- -------------------------------------------------------------
-- Query 6: Year-wise Average AQI and Record Counts
-- -------------------------------------------------------------
SELECT 
    record_year,
    COUNT(*) AS total_records,
    ROUND(AVG(index_value), 2) AS avg_aqi,
    MIN(index_value) AS min_aqi,
    MAX(index_value) AS max_aqi
FROM air_quality_records
GROUP BY record_year
ORDER BY record_year ASC;

-- -------------------------------------------------------------
-- Query 7: Month-wise AQI Trends (Seasonality Across All Years)
-- -------------------------------------------------------------
SELECT 
    record_month,
    COUNT(*) AS observation_count,
    ROUND(AVG(index_value), 2) AS avg_aqi,
    ROUND(STDDEV_POP(index_value), 2) AS stddev_aqi
FROM air_quality_records
GROUP BY record_month
ORDER BY record_month ASC;

-- -------------------------------------------------------------
-- Query 8: Seasonal AQI Analysis
-- -------------------------------------------------------------
SELECT 
    season,
    COUNT(*) AS total_records,
    ROUND(AVG(index_value), 2) AS avg_aqi,
    MIN(index_value) AS min_aqi,
    MAX(index_value) AS max_aqi
FROM air_quality_records
GROUP BY season
ORDER BY avg_aqi DESC;

-- -------------------------------------------------------------
-- Query 9: Air Quality Category Distribution
-- -------------------------------------------------------------
SELECT 
    air_quality,
    COUNT(*) AS category_count,
    ROUND(COUNT(*) * 100.0 / 299974, 2) AS percentage
FROM air_quality_records
GROUP BY air_quality
ORDER BY category_count DESC;

-- -------------------------------------------------------------
-- Query 10: Most Frequently Reported Prominent Pollutants
-- Note: Represents reporting frequency of prominent pollutants, not concentrations.
-- -------------------------------------------------------------
SELECT 
    individual_pollutant,
    COUNT(*) AS reporting_frequency,
    ROUND(COUNT(*) * 100.0 / 349147, 2) AS frequency_percentage
FROM v_individual_pollutants
GROUP BY individual_pollutant
ORDER BY reporting_frequency DESC;

-- -------------------------------------------------------------
-- Query 11: City-wise Pollutant Reporting Frequency (Sample Top Cities)
-- -------------------------------------------------------------
SELECT 
    city,
    individual_pollutant,
    COUNT(*) AS report_count
FROM v_individual_pollutants
WHERE city IN ('Delhi', 'Varanasi', 'Kanpur', 'Mumbai', 'Kolkata', 'Bengaluru', 'Hyderabad', 'Chennai')
GROUP BY city, individual_pollutant
ORDER BY city, report_count DESC;

-- -------------------------------------------------------------
-- Query 12: Cities with Highest Average AQI (Min 100 observations)
-- -------------------------------------------------------------
SELECT 
    city,
    ROUND(AVG(index_value), 2) AS avg_aqi,
    COUNT(*) AS observations
FROM air_quality_records
GROUP BY city
HAVING COUNT(*) >= 100
ORDER BY avg_aqi DESC
LIMIT 15;

-- -------------------------------------------------------------
-- Query 13: Highest and Lowest AQI Periods (Year-Month Level)
-- -------------------------------------------------------------
-- Top 5 Most Polluted Periods:
SELECT 
    concat(record_year, '-', lpad(record_month, 2, '0')) AS period_ym,
    ROUND(AVG(index_value), 2) AS avg_aqi,
    COUNT(*) AS observations
FROM air_quality_records
GROUP BY record_year, record_month
ORDER BY avg_aqi DESC
LIMIT 5;

-- Top 5 Cleanest Periods:
SELECT 
    concat(record_year, '-', lpad(record_month, 2, '0')) AS period_ym,
    ROUND(AVG(index_value), 2) AS avg_aqi,
    COUNT(*) AS observations
FROM air_quality_records
GROUP BY record_year, record_month
ORDER BY avg_aqi ASC
LIMIT 5;

-- -------------------------------------------------------------
-- Query 14: Year-over-Year (YoY) AQI Changes
-- -------------------------------------------------------------
WITH yearly_aqi AS (
    SELECT 
        record_year,
        ROUND(AVG(index_value), 2) AS avg_aqi
    FROM air_quality_records
    GROUP BY record_year
)
SELECT 
    record_year,
    avg_aqi,
    LAG(avg_aqi, 1) OVER (ORDER BY record_year) AS prev_year_aqi,
    ROUND(avg_aqi - LAG(avg_aqi, 1) OVER (ORDER BY record_year), 2) AS aqi_change,
    ROUND((avg_aqi - LAG(avg_aqi, 1) OVER (ORDER BY record_year)) * 100.0 / LAG(avg_aqi, 1) OVER (ORDER BY record_year), 2) AS pct_change
FROM yearly_aqi
ORDER BY record_year ASC;
