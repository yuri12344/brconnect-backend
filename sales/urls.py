# usuarios/urls.py

from django.urls import path
from .views import OrderView

urlpatterns = [
    path('', OrderView.as_view(), name='example')
    # outras rotas do app usuarios
]
