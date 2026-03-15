from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Avg
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from tutoringApp.apps.accounts.models import Profile, TutorProfile
from tutoringApp.apps.services.models import Review, Subject, TutoringSession
from tutoringApp.apps.services.forms import TutorAvailabilityForm


@login_required
def dashboard_redirect(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect("core:home")

    if profile.user_type == "student":
        return redirect("dashboard:student_dashboard")
    elif profile.user_type == "tutor":
        return redirect("dashboard:tutor_dashboard")
    elif profile.user_type == "app_admin":
        return redirect("dashboard:admin_dashboard")
    elif profile.user_type == "content_admin":
        return redirect("dashboard:content_admin")
    return redirect("core:home")


@login_required
def student_dashboard(request):
    now = timezone.now()
    profile = get_object_or_404(Profile, user=request.user)

    upcoming_sessions = TutoringSession.objects.filter(
        student=request.user,
        status="accepted",
        requested_datetime__gte=now,
    ).order_by("requested_datetime")

    past_sessions = TutoringSession.objects.filter(
        student=request.user,
        status="completed",
    ).select_related("subject", "tutor", "review").order_by("-requested_datetime")

    pending_sessions = TutoringSession.objects.filter(
        student=request.user,
        status="requested",
    )

    context = {
        "upcoming_sessions": upcoming_sessions,
        "past_sessions": past_sessions,
        "pending_sessions": pending_sessions,
        "profile": profile,
    }
    return render(request, "dashboard/student_dashboard.html", context)


@login_required
def tutor_dashboard(request):
    now = timezone.now()
    profile = get_object_or_404(Profile, user=request.user)

    upcoming_sessions = TutoringSession.objects.filter(
        tutor=request.user,
        status="accepted",
        requested_datetime__gte=now,
    ).order_by("requested_datetime")

    past_sessions = TutoringSession.objects.filter(
        tutor=request.user,
        status="completed",
    ).select_related("subject", "student", "review").order_by("-requested_datetime")

    reviews = Review.objects.filter(
        session__tutor=request.user,
    ).select_related("session__subject", "session__student").order_by("-created_at")[:10]

    avg_rating = Review.objects.filter(
        session__tutor=request.user,
    ).aggregate(avg=Avg("rating"))["avg"]

    context = {
        "upcoming_sessions": upcoming_sessions,
        "past_sessions": past_sessions,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "profile": profile,
    }
    return render(request, "dashboard/tutor_dashboard.html", context)


@login_required
def admin_dashboard(request):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.user_type != "app_admin":
        return redirect("dashboard:dashboard")

    total_users = User.objects.count()
    total_subjects = Subject.objects.count()
    total_sessions = TutoringSession.objects.count()
    total_tutors = Profile.objects.filter(user_type="tutor").count()

    recent_users = Profile.objects.select_related("user").order_by("-date_joined")[:10]
    tutors = TutorProfile.objects.select_related("profile__user").prefetch_related("subjects").all()

    context = {
        "total_users": total_users,
        "total_subjects": total_subjects,
        "total_sessions": total_sessions,
        "total_tutors": total_tutors,
        "recent_users": recent_users,
        "tutors": tutors,
    }
    return render(request, "dashboard/admin_dashboard.html", context)


@login_required
def content_admin_dashboard(request):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.user_type != "content_admin":
        return redirect("dashboard:dashboard")

    subjects = Subject.objects.all().order_by("name")
    context = {"subjects": subjects}
    return render(request, "dashboard/content_admin_dashboard.html", context)


# Subject CRUD for content admin
@login_required
def subject_create(request):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.user_type not in ("content_admin", "app_admin"):
        return redirect("dashboard:dashboard")

    from django.forms import ModelForm

    class SubjectForm(ModelForm):
        class Meta:
            model = Subject
            fields = ["name", "description"]

    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject created successfully.")
            return redirect("dashboard:content_admin")
    else:
        form = SubjectForm()

    return render(request, "dashboard/subject_form.html", {"form": form})


@login_required
def subject_edit(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.user_type not in ("content_admin", "app_admin"):
        return redirect("dashboard:dashboard")

    subject = get_object_or_404(Subject, pk=pk)

    from django.forms import ModelForm

    class SubjectForm(ModelForm):
        class Meta:
            model = Subject
            fields = ["name", "description"]

    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated successfully.")
            return redirect("dashboard:content_admin")
    else:
        form = SubjectForm(instance=subject)

    return render(request, "dashboard/subject_form.html", {"form": form, "subject": subject})


@login_required
def subject_delete(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.user_type not in ("content_admin", "app_admin"):
        return redirect("dashboard:dashboard")

    subject = get_object_or_404(Subject, pk=pk)

    if request.method == "POST":
        subject.delete()
        messages.success(request, "Subject deleted.")
        return redirect("dashboard:content_admin")

    return render(request, "dashboard/subject_confirm_delete.html", {"subject": subject})
