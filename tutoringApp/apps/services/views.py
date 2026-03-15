from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from tutoringApp.apps.accounts.decorators import student_required, tutor_required
from .models import TutoringSession, Review
from .forms import SessionRequestForm, ReviewForm
from .utils import haversine_distance


# ---------------------------------------------------------------------------
# Student views
# ---------------------------------------------------------------------------


@login_required
@student_required
def request_session(request):
    """Student requests a new tutoring session."""
    if request.method == "POST":
        form = SessionRequestForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.student = request.user
            session.save()
            messages.success(request, "Session requested successfully.")
            return redirect("services:my_requests")
    else:
        form = SessionRequestForm()

    return render(request, "services/request_session.html", {"form": form})


@login_required
@student_required
def my_requests(request):
    """List of sessions requested by the current student, with optional status filter."""
    status_filter = request.GET.get("status", "")
    sessions = TutoringSession.objects.filter(student=request.user).order_by(
        "-created_at"
    )
    if status_filter:
        sessions = sessions.filter(status=status_filter)

    return render(
        request,
        "services/my_requests.html",
        {
            "sessions": sessions,
            "current_status": status_filter,
            "status_choices": TutoringSession.Status.choices,
        },
    )


# ---------------------------------------------------------------------------
# Tutor views
# ---------------------------------------------------------------------------


@login_required
@tutor_required
def available_requests(request):
    """
    List open session requests, optionally filtered by distance from the
    tutor's location.
    """
    sessions = TutoringSession.objects.filter(
        status=TutoringSession.Status.REQUESTED
    ).order_by("-created_at")

    max_distance = request.GET.get("max_distance")
    tutor_lat = request.GET.get("lat")
    tutor_lon = request.GET.get("lon")

    if max_distance and tutor_lat and tutor_lon:
        try:
            max_km = float(max_distance)
            t_lat = float(tutor_lat)
            t_lon = float(tutor_lon)
        except (ValueError, TypeError):
            max_km = None

        if max_km is not None:
            filtered_ids = []
            for s in sessions:
                if s.latitude is not None and s.longitude is not None:
                    dist = haversine_distance(t_lat, t_lon, s.latitude, s.longitude)
                    if dist <= max_km:
                        filtered_ids.append(s.pk)
                else:
                    # Include sessions without coordinates (e.g. online)
                    filtered_ids.append(s.pk)
            sessions = sessions.filter(pk__in=filtered_ids)

    return render(
        request,
        "services/available_requests.html",
        {"sessions": sessions},
    )


@login_required
@tutor_required
def my_sessions(request):
    """List of sessions accepted by the current tutor."""
    sessions = TutoringSession.objects.filter(tutor=request.user).order_by(
        "-requested_datetime"
    )
    return render(
        request, "services/my_sessions.html", {"sessions": sessions}
    )


@login_required
@tutor_required
@require_POST
def accept_session(request, session_id):
    """AJAX endpoint for a tutor to accept a session request."""
    session = get_object_or_404(
        TutoringSession,
        pk=session_id,
        status=TutoringSession.Status.REQUESTED,
    )
    session.tutor = request.user
    session.status = TutoringSession.Status.ACCEPTED
    session.save()

    return JsonResponse(
        {"success": True, "message": "Session accepted successfully."}
    )


# ---------------------------------------------------------------------------
# Shared views
# ---------------------------------------------------------------------------


@login_required
def review_session(request, session_id):
    """Leave a review for a completed tutoring session."""
    session = get_object_or_404(
        TutoringSession, pk=session_id, status=TutoringSession.Status.COMPLETED
    )

    # Only the student or tutor of this session may leave a review
    if request.user not in (session.student, session.tutor):
        messages.error(request, "You are not authorized to review this session.")
        return redirect("services:my_requests")

    # Prevent duplicate reviews
    if Review.objects.filter(session=session, reviewer=request.user).exists():
        messages.info(request, "You have already reviewed this session.")
        return redirect("services:my_requests")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.session = session
            review.reviewer = request.user
            review.save()
            messages.success(request, "Review submitted successfully.")
            return redirect("services:my_requests")
    else:
        form = ReviewForm()

    return render(
        request,
        "services/review_session.html",
        {"form": form, "session": session},
    )
