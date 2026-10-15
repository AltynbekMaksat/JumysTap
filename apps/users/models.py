from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Role(models.TextChoices):
    JOB_SEEKER = "job_seeker", "Job Seeker"
    EMPLOYER = "employer", "Employer"

class User(AbstractUser):


        email = models.EmailField(unique=True)

        role = models.CharField(
            max_length=20,
            choices=Role.choices,
            default=Role.JOB_SEEKER,
        )

        def __str__(self) -> str:
            return self.username


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='job_seeker_profile',
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    city = models.CharField(
        max_length=20,
        blank=True,
    )

    bio = models.TextField(
        blank=True,

    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username} Profile'