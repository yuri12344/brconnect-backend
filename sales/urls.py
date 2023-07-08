from django.urls import path
from .views import HandleOrder

urlpatterns = [
    path('handle_order', HandleOrder.as_view(), name='handle_order')
]
