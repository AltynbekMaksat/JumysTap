import uuid
from django.db import models
from django.conf import settings


# Create your models here.
TITLE_MAX_LENGTH = 255
INSTITUTION_MAX_LENGTH = 255
DEGREE_MAX_LENGTH = 255
FIELD_OF_STUDY_MAX_LENGTH = 255
COMPANY_NAME_MAX_LENGTH = 255
SKILL_NAME_MAX_LENGTH = 255
STATUS_MAX_LENGTH = 50
APP_HISTORY_STATUS_MAX_LENGTH = 50
class Resume(models.Model):
    id = models.UUIDField (
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey (
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resumes"
    )
    title = models.CharField(
        max_length = TITLE_MAX_LENGTH,
    )
    summary = models.TextField(
        blank=True,
    )
    is_default = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add =True,
    )
    updated_at = models.DateTimeField(
        auto_now = True,
    )

class Education(models.Model):
    id = models.UUIDField (
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    resume = models.ForeignKey (
        to=Resume,
        on_delete=models.CASCADE,
        related_name="educations",
    )
    institution = models.CharField (
        max_length = INSTITUTION_MAX_LENGTH,
    )
    degree = models.CharField (
        max_length = DEGREE_MAX_LENGTH,
    )
    field_of_study = models.CharField (
        max_length = FIELD_OF_STUDY_MAX_LENGTH,
    )
    start_date = models.DateField (
        null=False,
        blank=False,
    )
    end_date = models.DateField (
        null=True,
        blank=True,
    )
    description = models.TextField (
        blank=True,
    )

class Experience(models.Model):
    id = models.UUIDField (
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    resume = models.ForeignKey (
        to=Resume,
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    company_name = models.CharField (
        max_length = COMPANY_NAME_MAX_LENGTH,
    )
    position = models.TextField (
        blank=True,
    )

class Skill(models.Model):
    id = models.UUIDField (
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField (
        max_length = SKILL_NAME_MAX_LENGTH,
        unique=True,
    )

class ResumeSkill(models.Model):
    id = models.UUIDField (
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    resume = models.ForeignKey (
        to=Resume,
        on_delete=models.CASCADE,
    )
    skill = models.ForeignKey (
        to=Skill,
        on_delete=models.CASCADE,
    )
    class Meta: 
        constraints = [
            models.UniqueConstraint (
                fields = ['resume', 'skill'],
                name = "unique_resume_skill",
            )
        ]
class ApplicationStatus (models.TextChoices):
    APPLIED = "applied", "Applied"
    VIEWED = "viewed", "Viewed"
    INTERVIEW = "interview", "Interview"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"

class Application(models.Model):
    id = models.UUIDField (
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey (
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    vacancy = models.ForeignKey (
        to="vacancies.Vacancy",
        on_delete=models.CASCADE,
    )
    resume = models.ForeignKey (
        to=Resume,
        on_delete=models.CASCADE,
    )
    status = models.CharField (
        max_length = STATUS_MAX_LENGTH,
        choices = ApplicationStatus.choices,
        default = ApplicationStatus.APPLIED,
    )
    cover_letter = models.TextField (
        blank=True,
    )
    created_at = models.DateTimeField (
        auto_now_add = True,
    )
    updated_at = models.DateTimeField (
        auto_now = True,
    )
    class Meta:
        constraints = [
            models.UniqueConstraint (
                fields=["user", "vacancy"],
                name="unique_user_vacancy_application",
            )
        ]

class ApplicationStatusHistory(models.Model):
    id = models.UUIDField (
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    application = models.ForeignKey (
        to=Application,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length = APP_HISTORY_STATUS_MAX_LENGTH,
        choices = ApplicationStatus.choices,
        null = True,
    )
    changed_at = models.DateTimeField (
        auto_now_add = True,
    )
    changed_by = models.ForeignKey (
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    comment = models.TextField (
        blank = True,
    )