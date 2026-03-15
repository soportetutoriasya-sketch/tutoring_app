from django.conf import settings


def google_maps_api_key(request):
    """Make the Google Maps API key available in all templates."""
    return {
        "GOOGLE_MAPS_API_KEY": getattr(settings, "GOOGLE_MAPS_API_KEY", ""),
    }
