from rest_framework.routers import DefaultRouter

from . import views

app_name = "notes:api"

router = DefaultRouter()
router.register("notes", views.NoteViewSet, basename="notes")
router.register("comments", views.CommentViewSet, basename="comments")

# urlpatterns = [
#     path("", views.NoteListCreateAPIView.as_view(), name="list"),
#     path("<int:note_id>", views.NoteDetailAPIView.as_view(), name="detail"),
# ]
