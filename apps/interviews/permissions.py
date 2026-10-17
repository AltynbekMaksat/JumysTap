from rest_framework.permissions import BasePermission

from apps.users.models import Role


class IsEmployer(BasePermission):
    message="Only employers are able to access this resource"

    def has_permission(self, request, view) ->bool:
        return request.user.is_authenticated and request.user.role==Role.EMPLOYER
