from typing import ClassVar

from rest_framework import serializers

from .models import Company, Review


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields: ClassVar[list] = [
            "id",
            "owner",
            "name",
            "description",
            "industry",
            "location",
            "created_at",
            "updated_at",
        ]
        read_only_fields: ClassVar[list] = [
            "id",
            "owner",
            "created_at",
            "updated_at",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields: ClassVar[list] = [
            "id",
            "company",
            "user",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields: ClassVar[list] = [
            "id",
            "company",
            "user",
            "created_at",
            "updated_at",
        ]
