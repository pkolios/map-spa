from django.conf import settings


def pass_config(request):
    """Return a dictionary of settings to be used in the templates."""
    return {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'GOOGLE_MAPS_TYPE': settings.GOOGLE_MAPS_TYPE,
        'GOOGLE_FUSION_URL': settings.GOOGLE_FUSION_URL,
    }
