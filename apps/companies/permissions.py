from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsEmployerOrReadOnly(BasePermission):
    message = "Only employers can create companies."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.role == "employer"


class IsCompanyOwnerOrReadOnly(BasePermission):
    message = "Only the company owner can edit this company."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and obj.owner_id == request.user.id


class IsReviewAuthorOrReadOnly(BasePermission):
    message = "Only the review author van edit this review."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and obj.user_id == request.user.id
