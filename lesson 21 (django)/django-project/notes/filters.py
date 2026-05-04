from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import QuerySet, Q, F
from django.db.models.functions import Substr

from .models import Note


def filter_notes_list(search: str) -> QuerySet[Note]:
    notes_qs = Note.objects.all()
    if search:
        notes_qs = notes_qs.filter(Q(title__icontains=search) | Q(content__icontains=search))

    # if search:
    #     vector = SearchVector("title", weight="A", config="russian") + SearchVector(
    #         "content", weight="B", config="russian"
    #     )
    #     query = SearchQuery(search, config="russian", search_type="websearch")
    #     notes_qs = notes_qs.annotate(
    #         vector=vector,
    #         rank=SearchRank(F("vector"), query),
    #         # trigram=TrigramSimilarity("title", search) + TrigramSimilarity("content", search),
    #     )
    #     # notes_qs = notes_qs.filter(Q(rank__gt=0.1) | Q(trigram__gt=0.1))
    #     notes_qs = notes_qs.filter(vector=query, rank__gt=0.1)
    #     notes_qs = notes_qs.order_by("-rank", "-created_at")

    notes_qs = notes_qs.select_related("user")  # JOIN с users только для FK.
    notes_qs = notes_qs.prefetch_related("tags")  # JOIN только для M2M.
    notes_qs = notes_qs.annotate(short_content=Substr("content", 1, 200))
    notes_qs = notes_qs.only("id", "title", "updated_at", "user__username")

    return notes_qs
