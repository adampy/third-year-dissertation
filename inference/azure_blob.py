from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions
from os import environ
from dotenv import load_dotenv

sas_token = None
sas_token_expiry = None
blob_service_client: BlobServiceClient = None

# Obtained from: https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-upload-python#upload-a-block-blob-from-a-local-file-path
def upload_blob_file(filename: str):
    init_sas_token()
    container_client = blob_service_client.get_container_client(container=environ.get("AZURE_CONTAINER_NAME"))
    with open(filename, mode="rb") as data:
        blob_client = container_client.upload_blob(name=filename, data=data, overwrite=True)
        
def load_blob_file(filename: str):
    init_sas_token()
    container_client = blob_service_client.get_container_client(container=environ.get("AZURE_CONTAINER_NAME"))
    with open(filename, mode="wb") as data:
        blob_client = container_client.download_blob(filename)
        data.write(blob_client.readall())
        
def init_sas_token():
    global sas_token, blob_service_client, sas_token_expiry # Globals are *generally* bad *if* we do not know where they are edited - here we do though
    
    # Load env vars
    load_dotenv()
    if environ.get("AZURE_CONTAINER_NAME") is None:
        raise ValueError("AZURE_CONTAINER_NAME environment variable not set")
    if environ.get("AZURE_ACCOUNT_NAME") is None:
        raise ValueError("AZURE_ACCOUNT_NAME environment variable not set")
    if environ.get("AZURE_ACCOUNT_KEY") is None:
        raise ValueError("AZURE_ACCOUNT_KEY environment variable not set")
    
    if not sas_token or not sas_token_expiry or datetime.utcnow() > sas_token_expiry:
        sas_token_expiry = datetime.utcnow() + timedelta(hours=1)
        sas_token = generate_account_sas(
            account_name=environ.get("AZURE_ACCOUNT_NAME"),
            account_key=environ.get("AZURE_ACCOUNT_KEY"),
            resource_types=ResourceTypes(service=True, container=True, object=True),
            permission=AccountSasPermissions(read=True, write=True, add=True, create=True, list=True, delete=True),
            expiry=sas_token_expiry
        )

        blob_service_client = BlobServiceClient(account_url=f"https://{environ.get('AZURE_ACCOUNT_NAME')}.blob.core.windows.net", credential=sas_token)