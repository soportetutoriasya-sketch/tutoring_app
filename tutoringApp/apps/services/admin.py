import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import (
    Subject,
    TutoringSession,
    Review,
    TutorReport,
    TutorAvailability,
)


def export_sessions_csv(modeladmin, request, queryset):
    """Export selected tutoring sessions to a CSV file."""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="tutoring_sessions.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            "ID",
            "Student",
            "Tutor",
            "Subject",
            "Mode",
            "Status",
            "Requested Datetime",
            "Duration (min)",
            "Price",
            "Location Address",
            "Latitude",
            "Longitude",
            "Meeting Link",
            "Notes",
            "Created At",
            "Updated At",
        ]
    )

    for session in queryset.select_related("student", "tutor", "subject"):
        writer.writerow(
            [
                session.id,
                session.student.get_full_name() or session.student.username,
                (
                    session.tutor.get_full_name() or session.tutor.username
                    if session.tutor
                    else ""
                ),
                session.subject.name,
                session.mode,
                session.status,
                session.requested_datetime.strftime("%Y-%m-%d %H:%M"),
                session.duration,
                session.price or "",
                session.location_address,
                session.latitude or "",
                session.longitude or "",
                session.meeting_link,
                session.notes,
                session.created_at.strftime("%Y-%m-%d %H:%M"),
                session.updated_at.strftime("%Y-%m-%d %H:%M"),
            ]
        )

    return response


export_sessions_csv.short_description = "Export selected sessions to CSV"


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(TutoringSession)
class TutoringSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject",
        "student",
        "tutor",
        "mode",
        "status",
        "requested_datetime",
        "duration",
        "price",
        "created_at",
    )
    list_filter = ("status", "mode", "subject", "created_at")
    search_fields = (
        "student__username",
        "student__first_name",
        "student__last_name",
        "tutor__username",
        "tutor__first_name",
        "tutor__last_name",
        "subject__name",
        "notes",
    )
    raw_id_fields = ("student", "tutor")
    actions = [export_sessions_csv]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("session", "reviewer", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = (
        "reviewer__username",
        "reviewer__first_name",
        "reviewer__last_name",
        "comment",
    )
    raw_id_fields = ("session", "reviewer")


@admin.register(TutorReport)
class TutorReportAdmin(admin.ModelAdmin):
    list_display = (
        "session",
        "student_progress_rating",
        "start_time",
        "end_time",
        "created_at",
    )
    list_filter = ("student_progress_rating", "created_at")
    search_fields = (
        "report_text",
        "strengths",
        "areas_for_improvement",
        "homework_assigned",
    )
    raw_id_fields = ("session",)


@admin.register(TutorAvailability)
class TutorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ("tutor", "day_of_week", "start_time", "end_time")
    list_filter = ("day_of_week",)
    search_fields = ("tutor__user__username", "tutor__user__first_name")
