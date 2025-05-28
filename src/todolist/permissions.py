from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == "admin"

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == "manager"

class IsAgent(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == "agent"
