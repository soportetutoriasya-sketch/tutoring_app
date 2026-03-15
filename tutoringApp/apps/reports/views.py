import csv
import io

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from tutoringApp.apps.accounts.models import Profile
from tutoringApp.apps.services.forms import TutorReportForm
from tutoringApp.apps.services.models import TutoringSession, TutorReport


@login_required
def tutor_write_report(request, session_id):
    """GET/POST form for a tutor to write a TutorReport for a specific session."""
    session = get_object_or_404(TutoringSession, pk=session_id)
    profile = Profile.objects.get(user=request.user)

    # Only tutors can write reports
    if profile.user_type != "tutor":
        raise Http404

    # Tutor must own the session
    if session.tutor != request.user:
        raise Http404

    if request.method == "POST":
        form = TutorReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.session = session
            report.save()
            return redirect("reports:view_report", report_id=report.pk)
    else:
        form = TutorReportForm()

    context = {
        "form": form,
        "session": session,
    }
    return render(request, "reports/write_report.html", context)


@login_required
def view_report(request, report_id):
    """View a specific tutor report.

    Students can view reports for their sessions.
    Tutors can view their own reports.
    """
    report = get_object_or_404(TutorReport, pk=report_id)
    profile = Profile.objects.get(user=request.user)

    # Students can view reports for their sessions
    if profile.user_type == "student":
        if report.session.student != request.user:
            raise Http404
    # Tutors can view their own reports
    elif profile.user_type == "tutor":
        if report.session.tutor != request.user:
            raise Http404
    else:
        raise Http404

    context = {
        "report": report,
        "session": report.session,
    }
    return render(request, "reports/view_report.html", context)


class Echo:
    """An object that implements just the write method of the file interface,
    used for streaming CSV rows."""

    def write(self, value):
        return value


@login_required
def admin_export_csv(request):
    """Export sessions as CSV filtered by date_from and date_to query params.

    Returns a StreamingHttpResponse. Login required, admin only.
    """
    profile = Profile.objects.get(user=request.user)
    if profile.user_type != "app_admin":
        raise Http404

    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    sessions = TutoringSession.objects.all().order_by("-created_at")

    if date_from:
        sessions = sessions.filter(requested_datetime__date__gte=date_from)
    if date_to:
        sessions = sessions.filter(requested_datetime__date__lte=date_to)

    def generate_rows():
        writer = csv.writer(Echo())
        yield writer.writerow([
            "ID",
            "Student",
            "Tutor",
            "Subject",
            "Mode",
            "Status",
            "Requested Datetime",
            "Duration (min)",
            "Price",
            "Location",
            "Created At",
        ])
        for session in sessions.iterator():
            yield writer.writerow([
                session.pk,
                session.student.username,
                session.tutor.username if session.tutor else "",
                session.subject.name,
                session.get_mode_display(),
                session.get_status_display(),
                session.requested_datetime.strftime("%Y-%m-%d %H:%M"),
                session.duration,
                str(session.price) if session.price is not None else "",
                session.location_address,
                session.created_at.strftime("%Y-%m-%d %H:%M"),
            ])

    response = StreamingHttpResponse(generate_rows(), content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="sessions_export.csv"'
    return response


@login_required
def admin_export_pdf(request):
    """Export sessions as PDF using reportlab.

    Filtered by date_from and date_to query params. Login required, admin only.
    """
    profile = Profile.objects.get(user=request.user)
    if profile.user_type != "app_admin":
        raise Http404

    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    sessions = TutoringSession.objects.all().order_by("-created_at")

    if date_from:
        sessions = sessions.filter(requested_datetime__date__gte=date_from)
    if date_to:
        sessions = sessions.filter(requested_datetime__date__lte=date_to)

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, height - 50, "Tutoring Sessions Report")

    pdf.setFont("Helvetica", 10)
    filter_text = "All sessions"
    if date_from and date_to:
        filter_text = f"From {date_from} to {date_to}"
    elif date_from:
        filter_text = f"From {date_from}"
    elif date_to:
        filter_text = f"Up to {date_to}"
    pdf.drawString(50, height - 70, filter_text)

    y = height - 100

    # Column headers
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(50, y, "ID")
    pdf.drawString(80, y, "Student")
    pdf.drawString(170, y, "Tutor")
    pdf.drawString(260, y, "Subject")
    pdf.drawString(350, y, "Status")
    pdf.drawString(420, y, "Date")
    pdf.drawString(510, y, "Duration")
    y -= 15

    pdf.setFont("Helvetica", 8)
    for session in sessions:
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 8)
            y = height - 50

        pdf.drawString(50, y, str(session.pk))
        pdf.drawString(80, y, session.student.username[:15])
        pdf.drawString(
            170, y, session.tutor.username[:15] if session.tutor else "N/A"
        )
        pdf.drawString(260, y, session.subject.name[:15])
        pdf.drawString(350, y, session.get_status_display())
        pdf.drawString(
            420, y, session.requested_datetime.strftime("%Y-%m-%d %H:%M")
        )
        pdf.drawString(510, y, f"{session.duration} min")
        y -= 14

    pdf.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="sessions_export.pdf"'
    return response
