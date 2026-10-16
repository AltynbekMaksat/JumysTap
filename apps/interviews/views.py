from django.utils import timezone
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.models import Role
from apps.users.permissions import IsJobSeeker


from .models import Interview
from .serializers import InterviewSerializer, InterviewFeedbackSerializer
from .permissions import IsEmployer
from .services import mark_applications_interview


class InterviewViewSet(viewsets.ModelViewSet):
    serializer_class=InterviewSerializer
    http_method_names=["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        user=self.request.user
        qs=Interview.objects.select_related("application__vacancy__company", "feedback")
        if user.is_staff:
            return qs
        if user.role==Role.EMPLOYER:
            return qs.filter(application__vacancy__company__owner=user)
        return qs.filter(application__user=user)

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            classes=[IsAuthenticated]
        elif self.action=="confirm":
            classes=[IsJobSeeker]
        else:
            classes=[IsEmployer]
        return [c() for c in classes]

    def perform_create(self, serializer):
        interview=serializer.save()
        mark_applications_interview(interview.application, self.request.user, interview)

    def perform_update(self, serializer):
        old=(serializer.instance.date, serializer.instance.start_time)
        interview=serializer.save()
        if (interview.date, interview.start_time)!=old:
            interview.confirmed_at=None
            interview.save(update_fields=["confirmed_at"])

    def _require_scheduled(self, interview):
        if interview.status!=Interview.Status.SCHEDULED:
            return Response(
                {"detail": "Interview is not in scheduled status"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return None

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        interview=self.get_object()
        error=self._require_scheduled(interview)
        if error:
            return error
        interview.status=Interview.Status.CANCELLED
        interview.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(interview).data)

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        interview=self.get_object()
        error=self._require_scheduled(interview)
        if error:
            return error
        interview.confirmed_at=timezone.now()
        interview.save(update_fields=["confirmed_at", "updated_at"])
        return Response(self.get_serializer(interview).data)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        """Record the interview result"""
        interview=self.get_object()
        error=self._require_scheduled(interview)
        if error:
            return error
        feedback=InterviewFeedbackSerializer(data=request.data)
        feedback.is_valid(raise_exception=True)
        with transaction.atomic():
            feedback.save(interview=interview, created_by=request.user)
            interview.status=Interview.Status.COMPLETED
            interview.save(update_fields=["status", "updated_at"])
        interview.refresh_from_db()
        return Response(self.get_serializer(interview).data)