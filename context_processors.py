
from django.conf import settings

def site_settings(request):
    return {
        "GEOAPIFY_API_KEY": getattr(
            settings, "GEOAPIFY_API_KEY", ""
        )
    }
