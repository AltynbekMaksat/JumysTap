from django.db import transaction
from apps.applications.models import ApplicationStatus, ApplicationStatusHistory

"""In Application there are statuses such as "viewed", "interview" it count as shortlisted """

SCHEDULABLE_STATUSES=tuple(
    s
    for s in (getattr(ApplicationStatus, "SHORTLISTED", None),
              ApplicationStatus.VIEWED,
              ApplicationStatus.INTERVIEW,
              )
    if s is not None
)

def mark_applications_interview(application, user, interview):
    """Move applications to Interview and write record in the history """
    if application.status==ApplicationStatus.INTERVIEW:
        return
    with transaction.atomic():
        application.status=ApplicationStatus.INTERVIEW
        application.save(update_fields=["status", "updated_at"])
        ApplicationStatusHistory.objects.create(
            application=application,
            status=ApplicationStatus.INTERVIEW,
            changed_by=user,
            comment=(
                f"Interview scheduled for {interview.date} "
                f"{interview.start_time:%H:%M}-{interview.end_time:%H:%M}"
            ),
        )
