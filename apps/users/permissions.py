from rest_framework.permissions import BasePermission

from .models import Role


class IsJobSeeker(BasePermission):
    message = "Only job seekers can access this resource."

    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated
            and request.user.role == Role.JOB_SEEKER
        )