from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TutoringSession(models.Model):
    class Mode(models.TextChoices):
        ONLINE = "online", "Online"
        IN_PERSON = "in_person", "In Person"

    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        ACCEPTED = "accepted", "Accepted"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_sessions",
        limit_choices_to={"profile__user_type": "student"},
    )
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tutor_sessions",
        null=True,
        blank=True,
        limit_choices_to={"profile__user_type": "tutor"},
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    mode = models.CharField(max_length=20, choices=Mode.choices)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.REQUESTED
    )
    requested_datetime = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    location_address = models.TextField(blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    meeting_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} - {self.student} ({self.status})"


class Review(models.Model):
    session = models.OneToOneField(
        TutoringSession, on_delete=models.CASCADE, related_name="review"
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.session} by {self.reviewer}"


class TutorReport(models.Model):
    session = models.ForeignKey(
        TutoringSession, on_delete=models.CASCADE, related_name="tutor_reports"
    )
    report_text = models.TextField()
    structured_content = models.JSONField(default=dict, blank=True)
    topics_covered = models.JSONField(default=list, blank=True)
    student_progress_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
    )
    student_progress_comments = models.TextField(blank=True)
    strengths = models.TextField(blank=True)
    areas_for_improvement = models.TextField(blank=True)
    homework_assigned = models.TextField(blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.session}"


class TutorAvailability(models.Model):
    class DayOfWeek(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"

    tutor = models.ForeignKey(
        "accounts.TutorProfile",
        on_delete=models.CASCADE,
        related_name="availabilities",
    )
    day_of_week = models.IntegerField(choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ("tutor", "day_of_week", "start_time")
        verbose_name_plural = "Tutor availabilities"

    def __str__(self):
        return (
            f"{self.tutor} - {self.get_day_of_week_display()} "
            f"{self.start_time} to {self.end_time}"
        )
