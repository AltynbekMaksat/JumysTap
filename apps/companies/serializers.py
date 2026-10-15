from rest_framework import serializers
from .models import Company, Review

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "owner",
            "name",
            "description",
            "industry",
            "location",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id", 
            "owner", 
            "created_at", 
            "updated_at",
        ]

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "company",
            "user",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "company",
            "user",
            "created_at",
            "updated_at"
        ]

   