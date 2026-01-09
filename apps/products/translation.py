from modeltranslation.translator import TranslationOptions, register

from apps.products.models import Product, ProductAttribute, ProductMedia, ProductVariant


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ("title", "description", "cta")


@register(ProductAttribute)
class ProductAttributeTranslationOptions(TranslationOptions):
    fields = ("name", "value")


@register(ProductMedia)
class ProductMediaTranslationOptions(TranslationOptions):
    fields = ("alt_text", "caption")


@register(ProductVariant)
class ProductVariantTranslationOptions(TranslationOptions):
    fields = ("size", "color")
