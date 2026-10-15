from rest_framework import generics, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Vacancy
from .serializers import VacancySerializer

class VacancyListCreateView(generics.ListCreateAPIView):
    queryset = Vacancy.objects.filter(is_active=True)
    serializer_class = VacancySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description", "requirements", "location"]
    ordering_fields = ["created_at", "salary_min", "salary_max"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        company = serializer.validated_data.get("company")

        if company.owner != self.request.user:
            raise PermissionDenied(
                "You can only create vacancies for your own company."
            )
        serializer.save()

class VacancyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VacancySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return Vacancy.objects.filter(company__owner=self.request.user)
        return Vacancy.objects.filter(is_active=True)