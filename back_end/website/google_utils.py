import os
import logging
import ast
from google.cloud import secretmanager, bigquery
from google.cloud import bigquery_storage
from google.oauth2 import service_account

def get_secret(secret_id):
    try:
        client = secretmanager.SecretManagerServiceClient()
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(name=secret_name)
        return response.payload.data.decode('UTF-8')
    except Exception as e:
        logging.error(f"Error accessing secret {secret_id}: {e}")
        raise e

def get_bigquery_client():
    project_id = os.getenv('gcp_project_id')
    service_account_file_path = os.getenv('gcp_credentials_path')
     # Create credentials using the service account key
    credentials = service_account.Credentials.from_service_account_file(service_account_file_path)
    
    # Set the credentials to the BigQuery client
    client = bigquery.Client(credentials=credentials, project=project_id)
    return client

def fetch_embeddings_from_bigquery(bq_client, dataset_name, table_name):
    query = f"""
        SELECT * FROM `{bq_client.project}.{dataset_name}.{table_name}`
    """
    # bq_storage_client = bigquery_storage.BigQueryReadClient()
    query_job = bq_client.query(query)
    results = query_job.result()
    df = results.to_dataframe()
    # df = results.to_dataframe(bqstorage_client=bq_storage_client)
    df['Embeddings'] = df['Embeddings'].apply(ast.literal_eval)  # Convert string representation of list to actual list
    return df
