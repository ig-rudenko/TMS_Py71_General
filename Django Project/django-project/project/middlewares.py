from uuid import uuid4

from django.conf import settings


class RequestIDMiddleware:

    def __init__(self, get_response):
        self.DEBUG = settings.DEBUG
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = request.META.get("HTTP_X_REQUEST_ID") or str(uuid4())

        print("AddRequestIDMiddleware", request.get_full_path(), "Request ID", request.request_id)

        response = self.get_response(request)

        response.headers["X-Request-ID"] = request.request_id

        return response
