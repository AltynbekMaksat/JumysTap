from django.contrib import admin
from .models import Interview, InterviewFeedBack
# Register your models here.


class InterviewFeedBackInline(admin.StackedInline):
    model=InterviewFeedBack
    extra=0


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display=("id",
                  "application",
                  "date",
                  "start_time",
                  "end_time",
                  "type",
                  "status",
                  )
    list_filter=("status",
                 "type",
                 "date")
    search_fields=("application__user__username",
                   "application__vacancy__title",
                   )
    inlines=[InterviewFeedBackInline]


@admin.register(InterviewFeedBack)
class InterviewFeedBackAdmin(admin.ModelAdmin):
    list_display=("interview",
                  "rating",
                  "recommendation",
                  "created_by",
                  "created_at",
                  )
    list_filter=("rating",
                 "recommendation",
                 )