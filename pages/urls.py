
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from . import views



urlpatterns = [
    path ('',views.index ),
    path ('index/', views.index),
    path('contact/', views.contact ),
    path('about', views.about),
]
