from rest_framework import serializers

from apps.categories.models import Category, Subcategory


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ("id", "label", "slug")


class CatalogCategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "label", "subcategories")

    def get_subcategories(self, obj: Category) -> list[str]:
        return [subcategory.label for subcategory in obj.subcategories.filter(is_active=True).order_by("sort_order")]
