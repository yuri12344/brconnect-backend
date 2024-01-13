from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from products.views import ProductViewSet
from sales.views import OrdersViewSet
from users.views import CustomerViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(r"orders", OrdersViewSet, basename="orders")
router.register(r"customers", CustomerViewSet, basename="customers")

urlpatterns = [
    path("token/", obtain_auth_token, name="api_token_auth"),
    path("", include("dj_rest_auth.urls")),
    path("sales/", include("sales.urls")),
    path("users/", include("users.urls")),
    path("", include(router.urls)),
]
