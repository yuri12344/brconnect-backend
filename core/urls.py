from rest_framework.authtoken.views import obtain_auth_token
from django.urls import include, path

urlpatterns = [
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('auth/', include('dj_rest_auth.urls')),

    path('sales/', include('sales.urls')),
    path('users/', include('users.urls')),
]

