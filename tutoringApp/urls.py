"""
URL configuration for tutoringApp project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("profile/", include("tutoringApp.apps.accounts.urls")),
    path("services/", include("tutoringApp.apps.services.urls")),
    path("dashboard/", include("tutoringApp.apps.dashboard.urls")),
    path("reports/", include("tutoringApp.apps.reports.urls")),
    path("", include("tutoringApp.apps.core.urls")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
