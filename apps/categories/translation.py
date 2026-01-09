from modeltranslation.translator import TranslationOptions, register

from apps.categories.models import Category, Subcategory


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("label", "description")


@register(Subcategory)
class SubcategoryTranslationOptions(TranslationOptions):
    fields = ("label",)
