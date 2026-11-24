-- hive/create_tables.hql
-- Sets up Hive external staging and managed ORC tables

USE air_quality_db;

-- 1. External Staging Table mapping CSV data in HDFS
DROP TABLE IF EXISTS air_quality_raw;

CREATE EXTERNAL TABLE IF NOT EXISTS air_quality_raw (
    record_date STRING,
    city STRING,
    no_stations STRING,
    air_quality STRING,
    index_value STRING,
    prominent_pollutant STRING,
    record_year STRING,
    record_month STRING,
    season STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
   "separatorChar" = ",",
   "quoteChar"     = "\"",
   "escapeChar"    = "\\"
)
LOCATION '/airquality/input/'
TBLPROPERTIES ("skip.header.line.count"="1");

-- 2. Managed High-Performance ORC Table
DROP TABLE IF EXISTS air_quality_records;

CREATE TABLE IF NOT EXISTS air_quality_records (
    record_date DATE,
    city STRING,
    no_stations INT,
    air_quality STRING,
    index_value INT,
    prominent_pollutant STRING,
    record_year INT,
    record_month INT,
    season STRING
)
STORED AS ORC
TBLPROPERTIES ("orc.compress"="SNAPPY");

-- 3. Populate ORC Table with Type Conversions
INSERT OVERWRITE TABLE air_quality_records
SELECT
    CAST(record_date AS DATE),
    trim(city),
    CAST(no_stations AS INT),
    trim(air_quality),
    CAST(index_value AS INT),
    trim(prominent_pollutant),
    CAST(record_year AS INT),
    CAST(record_month AS INT),
    trim(season)
FROM air_quality_raw
WHERE record_date IS NOT NULL 
  AND record_date != 'date'
  AND CAST(index_value AS INT) IS NOT NULL;

-- 4. Exploded Pollutants View for Multi-Pollutant Frequency Analysis
-- Splits comma-separated pollutants and normalizes whitespace
CREATE OR REPLACE VIEW v_individual_pollutants AS
SELECT
    record_date,
    city,
    index_value,
    air_quality,
    record_year,
    record_month,
    season,
    trim(single_pollutant) AS individual_pollutant
FROM air_quality_records
LATERAL VIEW explode(split(prominent_pollutant, ',\\s*')) t AS single_pollutant
WHERE trim(single_pollutant) != '' 
  AND trim(single_pollutant) != 'UNKNOWN';

SHOW TABLES;
DESCRIBE FORMATTED air_quality_records;
