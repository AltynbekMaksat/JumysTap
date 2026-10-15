from django.contrib import admin
from .models import JobCategory, Vacancy

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "category",
        "employment_type",
        "work_type",
        "is_active",
        "created_at",
    )
    list_filter = (
        "category",
        "employment_type",
        "work_type",
        "is_active",
    )
    search_fields = (
        "title",
        "description",
        "company__name",
    )
    list_select_related = ("company", "category")
    ordering = ("-created_at",)