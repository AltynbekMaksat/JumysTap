from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import(CompanyViewSet, CompanyReviewListCreateView, CompanyReviewDetailView,)

router = DefaultRouter()
router.register("", CompanyViewSet, basename = "company")


urlpatterns = [
    path(
        "<int:company_id>/reviews/",
        CompanyReviewListCreateView.as_view(),
    ),
    path(
        "<int:company_id>/reviews.<int:review_id>/",
        CompanyReviewDetailView.as_view(),
    ),
    path(
        "",
        include(router.urls),
    )
]