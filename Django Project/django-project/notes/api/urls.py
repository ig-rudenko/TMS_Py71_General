from django.urls import path

from . import views

app_name = "notes:api"

urlpatterns = [
    path("", views.notes_api_view, name="list"),
    path("<int:note_id>", views.note_detail_api_view, name="detail"),
]
