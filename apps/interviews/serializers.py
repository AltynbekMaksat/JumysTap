from datetime import datetime

from django.utils import timezone
from rest_framework import serializers
from apps.users.models import Role

from .models import Interview, InterviewFeedBack
from .services import SCHEDULABLE_STATUSES


class InterviewFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model=InterviewFeedBack
        fields=["id", "rating", "notes", "recommendation", "created_at", "updated_at"]
        read_only_fields=["id", "created_at", "updated_at"]


class InterviewSerializer(serializers.ModelSerializer):
    feedback=InterviewFeedbackSerializer(read_only=True)

    class Meta:
        model=Interview
        fields=[
            "id", "application", "date", "start_time", "end_time",
            "type", "location", "meeting_link", "status", "confirmed_at",
            "feedback", "created_at", "updated_at",
        ]

        read_only_fields=[
            "id", "status", "confirmed_at", "feedback", "created_at", "updated_at"
        ]

    def validate_application(self, application):
        user=self.context["request"].user
        if application.vacancy.company.owner_id!=user.id:
            raise serializers.ValidationError(
                "You can only schedule interviews for your own vacancies"
            )
        if not application.vacancy.is_active:
            raise serializers.ValidationError("This vacancy is no longer active")
        if application.status not in SCHEDULABLE_STATUSES:
            raise serializers.ValidationError(
                "Only shortlisted candidates can be invited to an interview"
            )
        return application

    def validate(self, attrs):
        instance=self.instance
        if instance:
            if instance.status!=Interview.Status.SCHEDULED:
                raise serializers.ValidationError(
                    "Only scheduled interviews can be changed!"
                )
            attrs.pop("application", None)

        def get(field):
            return attrs.get(field, getattr(instance, field, None))

        date, start, end=get("date"), get("start_time"), get("end_time")
        if end<=start:
            raise serializers.ValidationError(
                {"end_time": "End time must be after start time!"}
            )
        starts_at=timezone.make_aware(datetime.combine(date, start))
        if starts_at<=timezone.now():
            raise serializers.ValidationError(
                {"date": "Interview must be in the future!"}
            )
        itype=get("type")
        if itype==Interview.Type.ONLINE and not get("meeting_link"):
            raise serializers.ValidationError(
                {"meeting_link": "Meeting link is required for online interviews"}
            )
        if itype==Interview.Type.OFFLINE and not get("location"):
            raise serializers.ValidationError(
                {"location": "Location is required for offline interviews"}
            )
        return attrs

    def to_representation(self, instance):
        data=super().to_representation(instance)
        user=self.context["request"].user
        if not (user.is_staff or user.role==Role.EMPLOYER):
            data.pop("feedback", None)
        return data
                