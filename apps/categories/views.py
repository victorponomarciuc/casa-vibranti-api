from rest_framework.generics import ListAPIView

from apps.categories.models import Category
from apps.categories.serializers import CatalogCategorySerializer


class CategoryListAPIView(ListAPIView):
    serializer_class = CatalogCategorySerializer

    def get_queryset(self):
        return Category.objects.filter(is_active=True).prefetch_related("subcategories")
