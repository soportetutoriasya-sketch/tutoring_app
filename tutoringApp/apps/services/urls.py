from django.urls import path

from . import views

app_name = "services"

urlpatterns = [
    # Student URLs
    path(
        "request/",
        views.request_session,
        name="request_session",
    ),
    path(
        "my-requests/",
        views.my_requests,
        name="my_requests",
    ),
    # Tutor URLs
    path(
        "available/",
        views.available_requests,
        name="available_requests",
    ),
    path(
        "my-sessions/",
        views.my_sessions,
        name="my_sessions",
    ),
    path(
        "accept/<int:session_id>/",
        views.accept_session,
        name="accept_session",
    ),
    # Shared URLs
    path(
        "review/<int:session_id>/",
        views.review_session,
        name="review_session",
    ),
]
