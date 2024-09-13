from azure.storage.blob import BlobServiceClient
from django.conf import settings

def get_images_from_container(container_name):
    """
    Retrieves a list of image URLs from a specified Azure Blob Storage container.
    """
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(container_name)

    image_urls = []
    try:
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            if blob.name.endswith(('.jpg', '.jpeg', '.png')):
                image_url = f'https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net/{container_name}/{blob.name}'
                image_urls.append(image_url)
    except Exception:
        image_urls = []
    
    return image_urls


def get_blob_content(container_name, blob_name):
    """
    Retrieves the text content of a blob from the specified container.
    """
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(container_name)

    try:
        blob_client = container_client.get_blob_client(blob=blob_name)
        blob_data = blob_client.download_blob()
        content = blob_data.content_as_text()
    except Exception:
        content = "Content not found or error while retrieving it."
    
    return content
