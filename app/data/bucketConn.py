import os
import datetime
from google.cloud import storage
from google.oauth2 import service_account

from dotenv import load_dotenv
load_dotenv()

GOOGLE_APPLICATION_CREDENTIALS = service_account.Credentials.from_service_account_file(
    "/SECRETS/SERVICE_ACCOUNT"
)

bucket_name = os.environ.get("BUCKET_NAME")
service_account = os.environ.get("SERVICE_ACCOUNT")
project_id = os.environ.get("PROJECT_ID")

def get_bucket(bucket_name):
    client = storage.Client(credentials=GOOGLE_APPLICATION_CREDENTIALS)
    bucket = client.get_bucket(bucket_name)
    return bucket

def upload_blob_to_folder(source_file_name, destination_folder_name, destination_blob_name):
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(f"{destination_folder_name}/{destination_blob_name}")
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_folder_name}/{destination_blob_name}.")
    

def generate_presigned_url_for_profile(blob_name, expiration=3600):
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(f"userProfile/{blob_name}")
    url = blob.generate_signed_url(version="v4", expiration=datetime.timedelta(seconds=expiration), method='GET')
    return url

