from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD_CONFIG = {
    "SHOW_HISTORY": True,
    "SHOW_LANGUAGES": True,
    "SHOW_BACK_BUTTON": True,
    "SITE_HEADER": "Casa Vibranti Admin",
    "SITE_TITLE": "Casa Vibranti Admin Panel",
    "INDEX_TITLE": "Casa Vibranti Admin",
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {"ro": "ro", "ru": "ru"},
        },
    }
}