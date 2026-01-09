from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.categories.models import Category, Subcategory


class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 0
    fields = ("label", "slug", "sort_order", "is_active")
    ordering = ("sort_order", "label")


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ("label", "slug", "sort_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("label", "description")
    prepopulated_fields = {"slug": ("label",)}
    inlines = [SubcategoryInline]
    fieldsets = (
        (None, {"fields": ("label", "slug", "description")}),
        ("Visibility", {"fields": ("is_active", "sort_order")}),
    )


@admin.register(Subcategory)
class SubcategoryAdmin(TranslationAdmin):
    list_display = ("label", "category", "slug", "sort_order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("label", "category__label")
    prepopulated_fields = {"slug": ("label",)}
