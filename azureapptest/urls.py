
from django.contrib import admin
from django.urls import path
from azureapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('about-me/',views.about_me_view, name='about_me'), 
    path('upload/', views.upload_image, name='upload_image'),
    path('upload/success/', views.upload_success, name='upload_success'),
    path('travel/', views.travel_view, name='travel'),
    path('street/', views.street_view, name='street'),
    path('landscape/', views.landscape_view, name='landscape'),
    path('portrait/', views.portrait_view, name='portrait')
]
