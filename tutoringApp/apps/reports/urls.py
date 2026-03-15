from django.urls import path

from tutoringApp.apps.reports import views

app_name = "reports"

urlpatterns = [
    path("write/<int:session_id>/", views.tutor_write_report, name="tutor_write_report"),
    path("view/<int:report_id>/", views.view_report, name="view_report"),
    path("export/csv/", views.admin_export_csv, name="admin_export_csv"),
    path("export/pdf/", views.admin_export_pdf, name="admin_export_pdf"),
]
