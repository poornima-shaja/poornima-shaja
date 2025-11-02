from django.contrib import admin
from django.urls import path,views

urlpatterns = [
    path('shop/', views.index, name='shop'),
]
