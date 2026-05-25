from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return (
                request.user
                and request.user.is_authenticated
                and (request.user.is_staff or request.user.is_superuser)
            )

    def has_object_permission(self, request, view, obj):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or request.user.is_superuser)
        )


class IsAdminOrCreateOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        else:
            return (
                request.user
                and request.user.is_authenticated
                and (request.user.is_staff or request.user.is_superuser)
            )

    def has_object_permission(self, request, view, obj):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or request.user.is_superuser)
        )
