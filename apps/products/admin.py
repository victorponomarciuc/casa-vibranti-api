from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from unfold.admin import ModelAdmin, TabularInline

from apps.products.models import Product, ProductAttribute, ProductMedia, ProductVariant


class ProductMediaInline(TabularInline):
    model = ProductMedia
    extra = 0

    # Unfold sortable inlines
    ordering_field = "sort_order"
    hide_ordering_field = True  # keeps UI clean

    tab = True
    verbose_name = _("Media")
    verbose_name_plural = _("Media")

    fields = (
        "sort_order",
        "media_type",
        "file",
        "external_url",
        "poster",
        "alt_text",
        "caption",
        "is_primary",
        "preview",
    )
    readonly_fields = ("preview",)
    autocomplete_fields = ()  # keep if you have relations later

    @admin.display(description=_("Preview"))
    def preview(self, obj: ProductMedia) -> str:
        if obj and obj.file and obj.media_type == ProductMedia.MediaType.IMAGE:
            return format_html(
                '<img src="{}" style="max-height: 80px; border-radius: 10px;" />',
                obj.file.url,
            )
        return ""


class ProductVariantInline(TabularInline):
    model = ProductVariant
    extra = 0

    ordering_field = "sort_order"
    hide_ordering_field = True

    tab = True
    verbose_name = _("Variant")
    verbose_name_plural = _("Variants")

    fields = ("sort_order", "size", "color", "color_swatch", "sku", "price_override")
    # If size/color are FK -> can enable autocomplete:
    # autocomplete_fields = ("size", "color")


class ProductAttributeInline(TabularInline):
    model = ProductAttribute
    extra = 0

    ordering_field = "sort_order"
    hide_ordering_field = True

    tab = True
    verbose_name = _("Attribute")
    verbose_name_plural = _("Attributes")

    fields = ("sort_order", "name", "value")


@admin.register(Product)
class ProductAdmin(TranslationAdmin, ModelAdmin):
    list_display = ("title", "kind", "category", "subcategory", "price", "sale_price", "is_active")
    list_filter = ("kind", "category", "is_active")
    search_fields = ("title", "description", "category__label", "subcategory__label")
    autocomplete_fields = ("category", "subcategory")

    inlines = [ProductMediaInline, ProductVariantInline, ProductAttributeInline]

    fieldsets = (
        (
            _("Basics"),
            {
                "fields": ("kind", "title", "description", "category", "subcategory"),
                "description": _("Минимум обязательных полей, остальное — ниже в удобных блоках."),
            },
        ),
        (
            _("Pricing"),
            {
                "fields": ("price", "sale_price", "cta", "tags"),
                "description": _("Укажите цену и скидку. Теги помогают фильтрам на витрине."),
            },
        ),
        (
            _("Links"),
            {
                "fields": ("media_src", "poster", "href"),
                "classes": ("collapse",),
                "description": _("Ссылки для внешнего медиа, если не загружаете файлы."),
            },
        ),
        (
            _("Visibility"),
            {
                "fields": ("is_active",),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(ProductMedia)
class ProductMediaAdmin(TranslationAdmin, ModelAdmin):
    list_display = ("product", "media_type", "is_primary", "sort_order", "thumb")
    list_filter = ("media_type", "is_primary")
    search_fields = ("product__title", "alt_text", "caption")
    autocomplete_fields = ("product",)

    @admin.display(description=_("Preview"))
    def thumb(self, obj: ProductMedia) -> str:
        if obj.file and obj.media_type == ProductMedia.MediaType.IMAGE:
            return format_html(
                '<img src="{}" style="max-height: 42px; border-radius: 8px;" />',
                obj.file.url,
            )
        return "—"


@admin.register(ProductVariant)
class ProductVariantAdmin(TranslationAdmin, ModelAdmin):
    list_display = ("product", "size", "color", "sku", "price_override")
    list_filter = ("product",)
    search_fields = ("product__title", "sku", "size", "color")
    autocomplete_fields = ("product",)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(TranslationAdmin, ModelAdmin):
    list_display = ("product", "name", "value", "sort_order")
    list_filter = ("product",)
    search_fields = ("product__title", "name", "value")
    autocomplete_fields = ("product",)
