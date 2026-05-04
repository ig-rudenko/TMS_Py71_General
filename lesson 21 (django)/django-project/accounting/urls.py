from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "accounting"

urlpatterns = [
    path("register", views.register_user_view, name="register"),
    path("login", views.CustomLoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
]
