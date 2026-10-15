from django.contrib import admin

# Register your models here.
from unfold.admin import ModelAdmin

from .models import Company, Review


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    list_display = ("id", "name", "owner", "industry", "created_at")
    search_fields = ("name", "location", "industry")


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ("id", "company", "user", "rating", "created_at")
    list_filter = ("rating",)
