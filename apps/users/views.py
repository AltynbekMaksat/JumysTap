from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import JobSeekerProfile, User
from .permissions import IsJobSeeker
from .serializers import (
    JobSeekerProfileSerializer,
    RegisterSerializer,
    UserSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user


class JobSeekerProfileView(generics.GenericAPIView):
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def get(self, request) -> Response:
        profile = JobSeekerProfile.objects.filter(
            user=request.user
        ).first()

        if profile is None:
            raise NotFound("Job seeker profile does not exist.")

        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def post(self, request) -> Response:
        if JobSeekerProfile.objects.filter(
            user=request.user
        ).exists():
            return Response(
                {"detail": "Profile already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request) -> Response:
        profile = JobSeekerProfile.objects.filter(
            user=request.user
        ).first()

        if profile is None:
            raise NotFound("Job seeker profile does not exist.")

        serializer = self.get_serializer(
            profile,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)