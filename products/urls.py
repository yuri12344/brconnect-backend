from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, useCasesByProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'recomendations', useCasesByProductViewSet, basename='recomendacao')

urlpatterns = [
    path('', include(router.urls)),
]


