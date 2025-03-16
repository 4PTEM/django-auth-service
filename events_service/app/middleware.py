from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from rest_framework import status

class RoleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_role = request.headers.get("X-USER-ROLE")
        if not user_role or user_role.lower() not in ["user", "admin"]:
            return Response({'error': 'Invalid or missing X-USER-ROLE header'}, status=status.HTTP_403_FORBIDDEN)
