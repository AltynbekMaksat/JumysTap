from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Company, Review
from .serializers import CompanySerializer, ReviewSerializer
from .permissions import IsEmployerOrReadOnly, IsCompanyOwnerOrReadOnly, IsReviesAuthorOrReadOnly

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.select_related("owner").all()
    serializer_class = CompanySerializer
    permission_classes = [
        IsEmployerOrReadOnly,
        IsCompanyOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CompanyReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_company(self):
        return get_object_or_404(
            Company,
            pk = self.kwargs["company_id"],
        )
    
    def get_queryset(self):
        return Review.objects.filter(
            company  = self.get_company(),
        ).select_related("user", "company")
    
    def perform_create(self, serializer):
        serializer.save(
            company = self.get_company(),
            user = self.request.user,
        )

class CompanyReviewDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly, 
        IsReviesAuthorOrReadOnly,
    ]

    lookup_url_kwarg = "review_id"

    def get_queryset(self):
        return Review.objects.filter(
            company_id = self.kwargs["company_id"],
        ).select_related("user", "company")
    