from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        """
        The request is authenticated as an admin - read/write,
        if as a user - read-only request.
        SAFE_METHODS == ("GET", "HEAD", "OPTIONS")
        """

        return bool(
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        ) or (request.user and request.user.is_staff)
