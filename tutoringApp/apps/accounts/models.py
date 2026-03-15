from django.conf import settings
from django.db import models


class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ("student", "Student"),
        ("tutor", "Tutor"),
        ("app_admin", "App Admin"),
        ("content_admin", "Content Admin"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    user_firstname = models.TextField()
    user_lastname = models.TextField()
    user_cedulaid = models.TextField()
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    personal_references = models.JSONField(default=list, blank=True)
    bio = models.TextField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"


class TutorProfile(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="tutor_profile",
    )
    subjects = models.ManyToManyField(
        "services.Subject",
        blank=True,
    )
    is_verified = models.BooleanField(default=False)
    availability = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Tutor: {self.profile.user.username}"


class StudentProfile(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    grade_level = models.CharField(max_length=50, blank=True)
    interests = models.TextField(blank=True)

    def __str__(self):
        return f"Student: {self.profile.user.username}"


class InstituteProfile(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="institute_profile",
    )
    institute_name = models.TextField()
    owner_fullname = models.TextField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    availability = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Institute: {self.institute_name}"
