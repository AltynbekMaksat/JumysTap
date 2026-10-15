from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin

from .models import JobSeekerProfile, User


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "is_active",
        "date_joined",
    )

    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")

    fieldsets = BaseUserAdmin.fieldsets + (
        ("JumysTap", {"fields": ("role",)}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("JumysTap", {"fields": ("email", "role")}),
    )


@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(ModelAdmin):
    list_display = ("user", "phone", "city", "created_at")
    search_fields = ("user__username", "user__email", "city")
    list_filter = ("city",)
    readonly_fields = ("created_at",)