from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_techspire_admin)

class IsTechspireAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_techspire_admin)

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_techspire_admin:
            return True
        user_field = getattr(obj, 'user', None)
        return user_field == request.user
