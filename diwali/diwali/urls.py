# diwali/urls.py (Project-level)

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),  # URL for admin panel
    path('', include('myapp.urls')), 
]
