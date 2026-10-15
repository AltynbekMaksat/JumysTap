# Create your tests here.

from django.test import SimpleTestCase
from django.urls import resolve

from .views import CompanyReviewListCreateView, CompanyViewSet


class CompaniesURLTests(SimpleTestCase):
    def test_company_list_url(self):
        match = resolve("/api/companies/")
        self.assertIs(match.func.cls, CompanyViewSet)

    def test_company_reviews_url(self):
        match = resolve("/api/companies/1/reviews/")
        self.assertIs(match.func.view_class, CompanyReviewListCreateView)
