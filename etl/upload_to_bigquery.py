import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import mysql.connector
import sys

# GCP Configuration
GCP_PROJECT_ID = "mcap-project-477416"
BQ_DATASET = "yt_warehouse"
GCP_CREDENTIALS_PATH = r"C:\Users\samba\OneDrive\Desktop\Media_Content_Analytics_Platform\config\mcap-project-477416-81b2e0d3de01.json"

# MySQL Configuration
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "Samba@1925"
MYSQL_DB = "MEDIA_CONTENT_ANALYTICS"

# Authenticate BigQuery
try:
    credentials = service_account.Credentials.from_service_account_file(GCP_CREDENTIALS_PATH)
    bq_client = bigquery.Client(credentials=credentials, project=GCP_PROJECT_ID)
    print(f" Connected to BigQuery project: {GCP_PROJECT_ID}")
except Exception as e:
    print("Error connecting to BigQuery:", e)
    sys.exit(1)

# Connect to MySQL
try:
    mysql_conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
    print(f"Connected to MySQL database: {MYSQL_DB}")
except Exception as e:
    print("Error connecting to MySQL:", e)
    sys.exit(1)

cursor = mysql_conn.cursor()

# Define tables to upload
tables = ["yahoo_news_data", "youtube_data"]

# Loop and Upload Each Table
for table_name in tables:
    try:
        print(f"\n Reading data from MySQL table: {table_name} ...")

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        df = pd.DataFrame(rows, columns=columns)
        print(f" Retrieved {len(df)} rows from {table_name}")

        if df.empty:
            print(f" Skipping upload for {table_name}, table is empty.")
            continue

        # Define BigQuery table path
        bq_table_id = f"{GCP_PROJECT_ID}.{BQ_DATASET}.{table_name}"

        # Upload DataFrame to BigQuery
        print(f" Uploading to BigQuery table: {bq_table_id}")
        job = bq_client.load_table_from_dataframe(df, bq_table_id)
        job.result()  # Wait for completion

        print(f"Uploaded {len(df)} rows successfully to {bq_table_id}")

    except Exception as e:
        print(f"Error uploading {table_name}: {e}")

# Step 5: Close connections
cursor.close()
mysql_conn.close()
print("\n All tables uploaded successfully to BigQuery without errors!")
