from django.urls import path
from .views import LoginView

urlpatterns = [
    path('company/auth', LoginView.as_view()),
]
