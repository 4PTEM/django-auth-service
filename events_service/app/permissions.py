from rest_framework.permissions import BasePermission

class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        user_role = request.headers.get("X-USER-ROLE", "user").lower()
        print(f"User role: {user_role}")
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return user_role == 'admin'
        return True
