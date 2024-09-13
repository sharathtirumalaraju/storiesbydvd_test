from django.shortcuts import render
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

def home(request):
    travel_images = get_images_from_container('travel')
    return render(request, 'home.html', {'travel_images': travel_images})

