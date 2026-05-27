from djoser.conf import settings as djoser_settings
from drf_spectacular.utils import extend_schema

from .serializers import APITokenReturnSerializer

api_token_create_docs = extend_schema(
    request=djoser_settings.SERIALIZERS.token_create,
    responses={
        200: APITokenReturnSerializer,
    },
)
