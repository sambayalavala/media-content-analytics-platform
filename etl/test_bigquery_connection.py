# etl/test_bigquery_connection.py
from google.cloud import bigquery
from google.oauth2 import service_account

# ✅ Configuration
GCP_PROJECT_ID = "mcap-project-477416"
GCP_CREDENTIALS_PATH = r"C:\Users\samba\OneDrive\Desktop\Media_Content_Analytics_Platform\config\mcap-project-477416-81b2e0d3de01.json"
BQ_DATASET = "yt_warehouse"

# ✅ Create BigQuery client using service account
try:
    credentials = service_account.Credentials.from_service_account_file(GCP_CREDENTIALS_PATH)
    client = bigquery.Client(credentials=credentials, project=GCP_PROJECT_ID)
    print(f"✅ Successfully connected to BigQuery project: {GCP_PROJECT_ID}")
except Exception as e:
    print("❌ Failed to connect to BigQuery:", e)
    exit(1)

# ✅ List datasets
print("\n📦 Available Datasets in this project:")
datasets = list(client.list_datasets())
if datasets:
    for dataset in datasets:
        print(f" - {dataset.dataset_id}")
else:
    print("⚠️ No datasets found in this project.")

# ✅ Check if yt_warehouse dataset exists
dataset_ref = f"{GCP_PROJECT_ID}.{BQ_DATASET}"
try:
    dataset = client.get_dataset(dataset_ref)
    print(f"\n✅ Dataset '{BQ_DATASET}' exists and is accessible.")
except Exception as e:
    print(f"❌ Unable to access dataset '{BQ_DATASET}':", e)
    exit(1)

# ✅ List tables in dataset
print(f"\n📋 Tables in dataset '{BQ_DATASET}':")
try:
    tables = list(client.list_tables(dataset_ref))
    if tables:
        for table in tables:
            print(f" - {table.table_id}")
    else:
        print("⚠️ No tables found in this dataset.")
except Exception as e:
    print("❌ Error listing tables:", e)

print("\n🎯 BigQuery connection test complete.")
