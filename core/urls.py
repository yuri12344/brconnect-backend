# core/urls.py

from django.urls import include, path

urlpatterns = [
    path('products/', include('products.urls')),
    path('sales/', include('sales.urls')),
]

