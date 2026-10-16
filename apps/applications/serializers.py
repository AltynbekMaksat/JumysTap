from django.db import transaction
from rest_framework import serializers

from .models import (
    Application,
    ApplicationStatus,
    ApplicationStatusHistory,
)

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            "id",
            "vacancy",
            "resume",
            "cover_letter",
            "status",
            "created_at",
        ]
    def validate(self, attrs):
        user = self.context["request"].user
        vacancy = attrs["vacancy"]
        resume = attrs["resume"]

        if user.role != "job_seeker":
            raise serializers.ValidationError(
                "Only job seekers can apply for vacancies."
            )    

        if not vacancy.is_active:
            raise serializers.ValidationError(
                "This vacancy is no longer active."
            )

        if resume.user_id != user.pk:
            raise serializers.ValidationError(
                "You can apply using your own resume."
            )    

        if Application.objects.filter(
            user=user,
            vacancy=vacancy,
        ).exists():
            raise serializers.ValidationError(
            "You have already applied for this vacancy."
        )
        return attrs 

    @transaction.atomic
    def create(self,validated_data):
        user = self.context["request"].user

        application = Application.objects.create(
            user=user,
            status=ApplicationStatus.APPLIED,
            **validated_data,
        )

        ApplicationStatusHistory.objects.create(
            application=application,
            status=ApplicationStatus.APPLIED,
            changed_by=user,
            comment="Application submitted.",
        )
        return application