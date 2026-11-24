#!/bin/bash
# scripts/upload_to_hdfs.sh
# Reusable shell script to upload cleaned dataset to HDFS

CONTAINER="namenode"
LOCAL_CSV="dataset/processed/air_quality_cleaned.csv"
TMP_PATH="/tmp/air_quality_cleaned.csv"

echo "=== Creating HDFS Directories ==="
docker exec $CONTAINER hdfs dfs -mkdir -p /airquality/input
docker exec $CONTAINER hdfs dfs -mkdir -p /airquality/processed
docker exec $CONTAINER hdfs dfs -mkdir -p /airquality/output

echo "=== Copying CSV into NameNode Container ==="
docker cp $LOCAL_CSV $CONTAINER:$TMP_PATH

echo "=== Uploading CSV to HDFS ==="
docker exec $CONTAINER hdfs dfs -put -f $TMP_PATH /airquality/input/air_quality_cleaned.csv
docker exec $CONTAINER hdfs dfs -cp -f /airquality/input/air_quality_cleaned.csv /airquality/processed/air_quality_cleaned.csv

echo "=== Verifying HDFS Contents ==="
docker exec $CONTAINER hdfs dfs -ls -R /airquality
docker exec $CONTAINER hdfs dfs -du -h /airquality

echo "=== Checking Record Count in HDFS ==="
docker exec $CONTAINER bash -c "hdfs dfs -cat /airquality/input/air_quality_cleaned.csv | wc -l"
