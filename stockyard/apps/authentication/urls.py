from django.urls import path
from typing import List

from .views import RegistrationAPIView, LoginAPIView

app_name: str = 'authentication'
urlpatterns: List[path.__class__] = [
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
]
