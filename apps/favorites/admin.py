from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.favorites.models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ("user", "product", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__email", "product__title")
