from django.urls import path, re_path
from djoser.views import TokenDestroyView

from .views import ListCreateUserAPIView, CustomTokenCreateView

urlpatterns = [
    path("users/", ListCreateUserAPIView.as_view()),
    re_path(r"^token/login/?$", CustomTokenCreateView.as_view(), name="login"),
    re_path(r"^token/logout/?$", TokenDestroyView.as_view(), name="logout"),
]
