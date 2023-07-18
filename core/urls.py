# core/urls.py

from django.urls import include, path

urlpatterns = [
    path('sales/', include('sales.urls')),
    path('users/', include('users.urls')),
]

