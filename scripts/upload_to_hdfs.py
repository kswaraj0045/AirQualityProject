"""
scripts/upload_to_hdfs.py
Automates uploading the cleaned dataset to HDFS inside the Docker Hadoop cluster.
"""

import os
import subprocess
import sys

LOCAL_CLEANED_CSV = "dataset/processed/air_quality_cleaned.csv"
CONTAINER_NAME = "namenode"
CONTAINER_TEMP_PATH = "/tmp/air_quality_cleaned.csv"

HDFS_DIRS = [
    "/airquality",
    "/airquality/input",
    "/airquality/processed",
    "/airquality/output"
]
HDFS_TARGET_FILE = "/airquality/input/air_quality_cleaned.csv"

def run_command(cmd, description):
    print(f"--> {description}...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error ({result.returncode}):\n{result.stderr}")
        return False, result.stdout, result.stderr
    print(f"Success:\n{result.stdout.strip()}")
    return True, result.stdout, result.stderr

def upload_dataset():
    print("=" * 60)
    print("STARTING HDFS DATA INGESTION PIPELINE")
    print("=" * 60)

    if not os.path.exists(LOCAL_CLEANED_CSV):
        print(f"Error: Processed dataset not found at {LOCAL_CLEANED_CSV}")
        sys.exit(1)

    file_size_bytes = os.path.getsize(LOCAL_CLEANED_CSV)
    print(f"Local file confirmed: {LOCAL_CLEANED_CSV} ({file_size_bytes:,} bytes)")

    # 1. Create HDFS directories
    print("\n1. Creating HDFS directories:")
    for d in HDFS_DIRS:
        cmd = ["docker", "exec", CONTAINER_NAME, "hdfs", "dfs", "-mkdir", "-p", d]
        ok, out, err = run_command(cmd, f"Creating {d}")
        if not ok:
            sys.exit(1)

    # 2. Copy file into NameNode container temp
    print("\n2. Staging file into Hadoop NameNode container:")
    cmd = ["docker", "cp", LOCAL_CLEANED_CSV, f"{CONTAINER_NAME}:{CONTAINER_TEMP_PATH}"]
    ok, out, err = run_command(cmd, f"Copying to {CONTAINER_NAME}:{CONTAINER_TEMP_PATH}")
    if not ok:
        sys.exit(1)

    # 3. Put file into HDFS
    print("\n3. Ingesting file into HDFS:")
    cmd = ["docker", "exec", CONTAINER_NAME, "hdfs", "dfs", "-put", "-f", CONTAINER_TEMP_PATH, HDFS_TARGET_FILE]
    ok, out, err = run_command(cmd, f"Uploading to {HDFS_TARGET_FILE}")
    if not ok:
        sys.exit(1)

    # Also keep a copy in /airquality/processed/ for Hive external table mapping if needed
    cmd = ["docker", "exec", CONTAINER_NAME, "hdfs", "dfs", "-cp", "-f", HDFS_TARGET_FILE, "/airquality/processed/air_quality_cleaned.csv"]
    run_command(cmd, "Mirroring to /airquality/processed/")

    # 4. Verify in HDFS
    print("\n4. Verifying uploaded file in HDFS:")
    cmd = ["docker", "exec", CONTAINER_NAME, "hdfs", "dfs", "-ls", "-R", "/airquality"]
    ok, out, err = run_command(cmd, "Listing /airquality hierarchy")

    cmd = ["docker", "exec", CONTAINER_NAME, "hdfs", "dfs", "-du", "-h", "/airquality/"]
    ok, out, err = run_command(cmd, "Checking HDFS storage space usage")

    # 5. Check record count in HDFS
    print("\n5. Validating record count in HDFS:")
    count_cmd = ["docker", "exec", CONTAINER_NAME, "bash", "-c", f"hdfs dfs -cat {HDFS_TARGET_FILE} | wc -l"]
    ok, out, err = run_command(count_cmd, "Counting lines directly from HDFS stream")

    # 6. Preview records from HDFS
    print("\n6. Previewing records directly from HDFS stream:")
    preview_cmd = ["docker", "exec", CONTAINER_NAME, "bash", "-c", f"hdfs dfs -cat {HDFS_TARGET_FILE} | head -n 4"]
    ok, out, err = run_command(preview_cmd, "Reading head of HDFS file")

    print("=" * 60)
    print("HDFS INGESTION COMPLETED SUCCESSFULLY")
    print("=" * 60)

if __name__ == "__main__":
    upload_dataset()
