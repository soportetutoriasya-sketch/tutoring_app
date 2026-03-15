from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard_redirect, name="dashboard"),
    path("student/", views.student_dashboard, name="student_dashboard"),
    path("tutor/", views.tutor_dashboard, name="tutor_dashboard"),
    path("admin-panel/", views.admin_dashboard, name="admin_dashboard"),
    path("content/", views.content_admin_dashboard, name="content_admin"),
    path("content/subject/add/", views.subject_create, name="subject_create"),
    path("content/subject/<int:pk>/edit/", views.subject_edit, name="subject_edit"),
    path("content/subject/<int:pk>/delete/", views.subject_delete, name="subject_delete"),
]
