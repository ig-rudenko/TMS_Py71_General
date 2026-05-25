from django.urls import path, include

from .views import ListCreateUserAPIView

urlpatterns = [
    path("users/", ListCreateUserAPIView.as_view()),
    path("", include("djoser.urls.authtoken")),
]
