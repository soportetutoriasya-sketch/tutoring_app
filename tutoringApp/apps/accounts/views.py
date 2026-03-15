from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Profile, TutorProfile, StudentProfile, InstituteProfile
from .forms import ProfileForm, TutorProfileForm, StudentProfileForm, InstituteProfileForm


@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    context = {"profile": profile}

    if profile.user_type == "tutor":
        tutor_profile = getattr(profile, "tutor_profile", None)
        context["tutor_profile"] = tutor_profile
    elif profile.user_type == "student":
        student_profile = getattr(profile, "student_profile", None)
        context["student_profile"] = student_profile

    return render(request, "accounts/profile.html", context)


@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)

    # Determine the type-specific form and instance
    type_form_class = None
    type_instance = None

    if profile.user_type == "tutor":
        type_form_class = TutorProfileForm
        type_instance, _ = TutorProfile.objects.get_or_create(profile=profile)
    elif profile.user_type == "student":
        type_form_class = StudentProfileForm
        type_instance, _ = StudentProfile.objects.get_or_create(profile=profile)
    elif profile.user_type in ("app_admin", "content_admin"):
        # Admins may have an institute profile
        try:
            type_instance = profile.institute_profile
            type_form_class = InstituteProfileForm
        except InstituteProfile.DoesNotExist:
            type_form_class = None

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        type_form = (
            type_form_class(request.POST, request.FILES, instance=type_instance)
            if type_form_class
            else None
        )

        forms_valid = profile_form.is_valid()
        if type_form:
            forms_valid = forms_valid and type_form.is_valid()

        if forms_valid:
            profile_form.save()
            if type_form:
                sub_profile = type_form.save(commit=False)
                sub_profile.profile = profile
                sub_profile.save()
                type_form.save_m2m()
            return redirect("accounts:profile")
    else:
        profile_form = ProfileForm(instance=profile)
        type_form = (
            type_form_class(instance=type_instance)
            if type_form_class
            else None
        )

    context = {
        "profile_form": profile_form,
        "type_form": type_form,
        "profile": profile,
    }
    return render(request, "accounts/profile_edit.html", context)
