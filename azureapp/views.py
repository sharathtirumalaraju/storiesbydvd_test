from django.shortcuts import render, redirect
from django.conf import settings
from azure.storage.blob import BlobServiceClient
from .forms import ImageUploadForm
import os

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            container = request.POST.get('container')  # Get the selected container
            
            # Validate container selection
            if container not in ['street', 'travel', 'landscape', 'portrait']:
                return render(request, 'upload.html', {'form': form, 'error': 'Invalid container selected'})

            # Create BlobServiceClient with the connection string
            blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_CONNECTION_STRING)
            blob_client = blob_service_client.get_blob_client(container=container, blob=image.name)
            
            # Upload the image to the selected container
            blob_client.upload_blob(image, overwrite=True)

            return redirect('upload_success')
    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})

def upload_success(request):
    return render(request, 'upload_success.html')