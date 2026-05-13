from django.urls import path

from . import views

app_name = "notes:api"

urlpatterns = [
    path("", views.NoteListCreateAPIView.as_view(), name="list"),
    path("<int:note_id>", views.NoteDetailAPIView.as_view(), name="detail"),
]
