
from django.contrib import admin
from django.urls import path
from azureapp import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('upload/success/', views.upload_success, name='upload_success')
]

