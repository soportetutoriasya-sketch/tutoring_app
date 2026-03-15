from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field

from .models import TutoringSession, Review, TutorReport, TutorAvailability


class SessionRequestForm(forms.ModelForm):
    class Meta:
        model = TutoringSession
        fields = [
            "subject",
            "mode",
            "requested_datetime",
            "duration",
            "location_address",
            "latitude",
            "longitude",
            "notes",
            "meeting_link",
        ]
        widgets = {
            "requested_datetime": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "location_address": forms.Textarea(attrs={"rows": 2}),
            "notes": forms.Textarea(attrs={"rows": 3}),
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["requested_datetime"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "subject",
            "mode",
            Row(
                Column("requested_datetime", css_class="col-md-6"),
                Column("duration", css_class="col-md-6"),
            ),
            "location_address",
            "latitude",
            "longitude",
            "meeting_link",
            "notes",
            Submit("submit", "Request Session", css_class="btn btn-primary"),
        )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "comment": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit("submit", "Submit Review", css_class="btn btn-primary")
        )


class TutorReportForm(forms.ModelForm):
    class Meta:
        model = TutorReport
        fields = [
            "report_text",
            "structured_content",
            "topics_covered",
            "student_progress_rating",
            "student_progress_comments",
            "strengths",
            "areas_for_improvement",
            "homework_assigned",
            "start_time",
            "end_time",
            "location",
        ]
        widgets = {
            "report_text": forms.Textarea(attrs={"rows": 5}),
            "student_progress_comments": forms.Textarea(attrs={"rows": 3}),
            "strengths": forms.Textarea(attrs={"rows": 3}),
            "areas_for_improvement": forms.Textarea(attrs={"rows": 3}),
            "homework_assigned": forms.Textarea(attrs={"rows": 3}),
            "start_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
            "end_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
            "student_progress_rating": forms.NumberInput(
                attrs={"min": 1, "max": 5}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "report_text",
            Row(
                Column("start_time", css_class="col-md-4"),
                Column("end_time", css_class="col-md-4"),
                Column("location", css_class="col-md-4"),
            ),
            "topics_covered",
            "structured_content",
            Row(
                Column("student_progress_rating", css_class="col-md-4"),
                Column("student_progress_comments", css_class="col-md-8"),
            ),
            "strengths",
            "areas_for_improvement",
            "homework_assigned",
            Submit("submit", "Submit Report", css_class="btn btn-primary"),
        )


class TutorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = TutorAvailability
        fields = ["day_of_week", "start_time", "end_time"]
        widgets = {
            "start_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
            "end_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "day_of_week",
            Row(
                Column("start_time", css_class="col-md-6"),
                Column("end_time", css_class="col-md-6"),
            ),
            Submit("submit", "Save Availability", css_class="btn btn-primary"),
        )
