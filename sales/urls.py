from django.urls import path
from . import views


urlpatterns = [
    path('handle_order', views.HandleOrder.as_view(), name='handle_order'),
]
