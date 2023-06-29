# usuarios/urls.py

from django.urls import path
from .views import SaleView

urlpatterns = [
    path('', SaleView.as_view(), name='example')
    # outras rotas do app usuarios
]
