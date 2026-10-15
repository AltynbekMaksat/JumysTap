from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import JobSeekerProfileView, RegisterView, UserMeView

app_name = "users"

urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "me/",
        UserMeView.as_view(),
        name="user_me",
    ),
    path(
        "profile/",
        JobSeekerProfileView.as_view(),
        name="job_seeker_profile",
    ),
]