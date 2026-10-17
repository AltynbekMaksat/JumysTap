from django.contrib import admin


from .models import (
    Resume,
    Education,
    Experience,
    Skill,
    ResumeSkill,
    Application,
    ApplicationStatusHistory,
)


class EducationInline(admin.TabularInline):
    model = Education
    extra = 0


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0


class ResumeSkillInline(admin.TabularInline):
    model = ResumeSkill
    extra = 0


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "is_default", "created_at", "updated_at")
    list_filter = ("is_default", "created_at")
    search_fields = ("title", "user__username", "user__email")
    readonly_fields = ("id", "created_at", "updated_at")
    inlines = [EducationInline, ExperienceInline, ResumeSkillInline]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("institution", "degree", "field_of_study", "resume")
    search_fields = ("institution", "degree", "field_of_study")
    readonly_fields = ("id",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("company_name", "position", "resume")
    search_fields = ("company_name", "position")
    readonly_fields = ("id",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("id",)


@admin.register(ResumeSkill)
class ResumeSkillAdmin(admin.ModelAdmin):
    list_display = ("resume", "skill")
    search_fields = ("resume__title", "skill__name")
    readonly_fields = ("id",)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "vacancy",
        "resume",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "created_at")
    search_fields = (
        "user__username",
        "user__email",
        "vacancy__title",
        "resume__title",
    )
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(ApplicationStatusHistory)
class ApplicationStatusHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "status",
        "changed_by",
        "changed_at",
    )
    list_filter = ("status", "changed_at")
    search_fields = (
        "application__user__username",
        "application__vacancy__title",
        "changed_by__username",
        "comment",
    )
    readonly_fields = ("id", "changed_at")

