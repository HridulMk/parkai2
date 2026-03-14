from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Allows read-only access to everyone,
    but write access only to admin users.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsVendorOrAdmin(BasePermission):
    """
    Allows access to vendor users or admin users.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        if getattr(request.user, 'user_type', None) in {'vendor', 'admin'}:
            return True

        return False


class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission.
    Only owner or admin can modify.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True

        return obj.user == request.user


class IsAdminUserType(BasePermission):
    """
    Allows access only to admin users.
    Supports both custom user_type='admin' and Django is_staff admins.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        return getattr(request.user, 'user_type', None) == 'admin'
