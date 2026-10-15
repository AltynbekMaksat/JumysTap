from typing import ClassVar

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Company(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="companies",
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ClassVar[list] = ["-created_at"]
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Review(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_reviews",
    )

    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ClassVar[list] = ["-created_at"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        constraints: ClassVar[list] = [
            models.UniqueConstraint(
                fields=["company", "user"],
                name="unique_company_review_per_user",
            ),
        ]

    def __str__(self):
        return f"{self.company.name} - {self.rating}/5"
