from django.shortcuts import render, redirect
from django.conf import settings
from azure.storage.blob import BlobServiceClient
from .forms import ImageUploadForm
from .helper import get_images_from_container,get_blob_content
import os

def home(request):
    return render(request, 'home.html')

def portfolio_view(request):
    return render(request, 'portfolio.html')

def about_me_view(request):
    about_me_content = get_blob_content('aboutme', 'about_me.txt')
    return render(request, 'about_me.html', {'about_me_content': about_me_content})

def travel_view(request):
    travel_images = get_images_from_container('travel')
    return render(request, 'travel.html', {'travel_images': travel_images})

def street_view(request):
    street_images = get_images_from_container('street')
    return render(request, 'street.html', {'street_images': street_images})

def landscape_view(request):
    landscape_images = get_images_from_container('landscape')
    return render(request, 'landscape.html', {'landscape_images': landscape_images})

def portrait_view(request):
    portrait_images = get_images_from_container('portrait')
    return render(request, 'portrait.html', {'portrait_images': portrait_images})

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
            if not settings.AZURE_CONNECTION_STRING:
                return render(request, 'upload.html', {'form': form, 'error': 'Azure connection string not configured properly'})

            blob_client = blob_service_client.get_blob_client(container=container, blob=image.name)
            
            # Upload the image to the selected container
            try:
                blob_client.upload_blob(image, overwrite=True)
            except Exception as e:
                return render(request, 'upload.html', {'form': form, 'error': f"Failed to upload image: {str(e)}"})

            return redirect('upload_success')
    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})


def upload_success(request):
    return render(request, 'upload_success.html')
