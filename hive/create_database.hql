-- hive/create_database.hql
-- Creates the Hive database for air quality analysis

CREATE DATABASE IF NOT EXISTS air_quality_db
COMMENT 'Spatio-Temporal Air Quality and Dominant Pollutant Analysis'
LOCATION '/airquality/database/';

SHOW DATABASES;
