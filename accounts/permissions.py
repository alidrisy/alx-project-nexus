from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'role', None) == 'ADMIN')


class IsRecruiterOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'role', None) in ('RECRUITER', 'ADMIN'))


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        owner = getattr(obj, 'posted_by', None) or getattr(obj, 'candidate', None)
        return owner == request.user or getattr(request.user, 'role', None) == 'ADMIN' 