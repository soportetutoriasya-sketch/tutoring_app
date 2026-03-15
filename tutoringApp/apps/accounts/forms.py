from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Profile, TutorProfile, StudentProfile, InstituteProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user", "date_joined"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save Profile"))


class TutorProfileForm(forms.ModelForm):
    class Meta:
        model = TutorProfile
        exclude = ["profile"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save Tutor Profile"))


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ["profile"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save Student Profile"))


class InstituteProfileForm(forms.ModelForm):
    class Meta:
        model = InstituteProfile
        exclude = ["profile"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save Institute Profile"))
