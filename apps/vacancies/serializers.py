from rest_framework import serializers
from .models import JobCategory, Vacancy


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = "__all__"

class VacancySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(
        source='company.name',
        read_only=True,
    )
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )
    class Meta:
        model = Vacancy
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")