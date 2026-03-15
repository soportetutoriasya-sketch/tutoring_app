import json

from django.shortcuts import render
from django.contrib import messages

from tutoringApp.apps.core.forms import ContactForm


def home(request):
    """Home page view. Shows featured subjects and nearby tutors for authenticated students."""
    from tutoringApp.apps.services.models import Subject
    from tutoringApp.apps.accounts.models import Profile, TutorProfile

    subjects = Subject.objects.all()
    tutors_data = None

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile.user_type == "student":
                # Get all verified tutors with coordinates for the map
                tutors = TutorProfile.objects.filter(
                    is_verified=True,
                    profile__latitude__isnull=False,
                    profile__longitude__isnull=False,
                )
                tutor_list = []
                for t in tutors:
                    tutor_list.append({
                        "name": t.profile.user_firstname + " " + t.profile.user_lastname,
                        "latitude": t.profile.latitude,
                        "longitude": t.profile.longitude,
                        "subjects": ", ".join(s.name for s in t.subjects.all()),
                    })
                if tutor_list:
                    tutors_data = json.dumps(tutor_list)
        except Profile.DoesNotExist:
            pass

    context = {
        "subjects": subjects,
        "tutors_data": tutors_data,
    }
    return render(request, "core/home.html", context)


def about(request):
    return render(request, "core/about.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Thank you for your message. We will get back to you shortly.")
            form = ContactForm()
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})
