import uuid
from django.db import models

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Interview(models.Model):
    """So structure of interview"""

    class Type(models.TextChoices):
        ONLINE="online", "Online"
        OFFLINE="offline", "Offline"
        PHONE="phone", "Phone"

    class Status(models.TextChoices):
        SCHEDULED="scheduled", "Scheduled"
        COMPLETED="completed", "Completed"
        CANCELLED="cancelled", "Cancelled"

    """Interview and Application are connected so we get application_id"""

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application=models.ForeignKey(
        "applications.Application",
        on_delete=models.CASCADE,
        related_name="interviews"
    )

    date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()

    MAX_TYPE=50
    MAX_LOCATION=255
    MAX_STATUS=50
    MAX_URL=500

    type=models.CharField(max_length=MAX_TYPE, choices=Type.choices)

    location=models.CharField(max_length=MAX_LOCATION, blank=True)

    meeting_link=models.URLField(max_length=MAX_URL, blank=True)

    status=models.CharField(
        max_length=MAX_STATUS, choices=Status.choices, default=Status.SCHEDULED
    )

    confirmed_at=models.DateTimeField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=["date", "start_time"]

    def __str__(self):
        return f"Interview {self.id} ({self.date} {self.start_time}, {self.status})"


class InterviewFeedBack(models.Model):
    class Recommendation(models.TextChoices):
        HIRE="hire", "Hire"
        MAYBE="maybe", "Maybe"
        NO_HIRE="no_hire", "Do not hire"

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    interview=models.OneToOneField(
        Interview,
        on_delete=models.CASCADE,
        related_name="feedback",
    )

    MAX_REC=20

    rating=models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    notes=models.TextField(blank=True)
    recommendation=models.CharField(max_length=MAX_REC, choices=Recommendation.choices)
    created_by=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="interview_feedbacks",
    )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name="Interview feedback"
        verbose_name_plural="Interviews feedback"

    def __str__(self):
        return f"Feedback for {self.interview_id}: {self.rating}/5 ({self.recommendation})"




