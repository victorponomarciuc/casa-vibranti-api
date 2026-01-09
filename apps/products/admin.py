from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
import nested_admin

from apps.products.models import Product, ProductAttribute, ProductMedia, ProductVariant


class ProductMediaInline(nested_admin.NestedTabularInline):
    model = ProductMedia
    extra = 0
    sortable_field_name = "sort_order"
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

    def preview(self, obj: ProductMedia) -> str:
        if obj.file and obj.media_type == ProductMedia.MediaType.IMAGE:
            return format_html('<img src="{}" style="max-height: 80px;" />', obj.file.url)
        return ""

    preview.short_description = "Preview"


class ProductVariantInline(nested_admin.NestedTabularInline):
    model = ProductVariant
    extra = 0
    sortable_field_name = "sort_order"
    fields = ("sort_order", "size", "color", "color_swatch", "sku", "price_override")


class ProductAttributeInline(nested_admin.NestedTabularInline):
    model = ProductAttribute
    extra = 0
    sortable_field_name = "sort_order"
    fields = ("sort_order", "name", "value")


@admin.register(Product)
class ProductAdmin(TranslationAdmin, nested_admin.NestedModelAdmin):
    list_display = ("title", "kind", "category", "subcategory", "price", "sale_price", "is_active")
    list_filter = ("kind", "category", "is_active")
    search_fields = ("title", "description", "category__label", "subcategory__label")
    autocomplete_fields = ("category", "subcategory")
    inlines = [ProductMediaInline, ProductVariantInline, ProductAttributeInline]
    fieldsets = (
        (
            "Basics",
            {
                "fields": ("kind", "title", "description", "category", "subcategory"),
                "description": "Минимум обязательных полей, остальное — ниже в удобных блоках.",
            },
        ),
        (
            "Pricing",
            {
                "fields": ("price", "sale_price", "cta", "tags"),
                "description": "Укажите цену и скидку. Теги помогают фильтрам на витрине.",
            },
        ),
        (
            "Links",
            {
                "fields": ("media_src", "poster", "href"),
                "classes": ("collapse",),
                "description": "Ссылки для внешнего медиа, если не загружаете файлы.",
            },
        ),
        (
            "Visibility",
            {"fields": ("is_active",), "classes": ("collapse",)},
        ),
    )


@admin.register(ProductMedia)
class ProductMediaAdmin(TranslationAdmin):
    list_display = ("product", "media_type", "is_primary", "sort_order")
    list_filter = ("media_type", "is_primary")
    search_fields = ("product__title", "alt_text", "caption")


@admin.register(ProductVariant)
class ProductVariantAdmin(TranslationAdmin):
    list_display = ("product", "size", "color", "sku", "price_override")
    list_filter = ("product",)
    search_fields = ("product__title", "sku", "size", "color")


@admin.register(ProductAttribute)
class ProductAttributeAdmin(TranslationAdmin):
    list_display = ("product", "name", "value", "sort_order")
    list_filter = ("product",)
    search_fields = ("product__title", "name", "value")
