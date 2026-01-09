from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.products.models import Product
from apps.products.serializers import CatalogProductDetailSerializer, CatalogProductSerializer


class ProductFilterSet(filters.FilterSet):
    category = filters.CharFilter(method="filter_category")
    subcategory = filters.CharFilter(method="filter_subcategory")
    minPrice = filters.NumberFilter(field_name="price", lookup_expr="gte")
    maxPrice = filters.NumberFilter(field_name="price", lookup_expr="lte")
    discounted = filters.BooleanFilter(method="filter_discounted")

    class Meta:
        model = Product
        fields = ("category", "subcategory", "minPrice", "maxPrice", "discounted")

    def filter_category(self, queryset, name, value):
        return queryset.filter(Q(category__label__iexact=value) | Q(category__slug__iexact=value))

    def filter_subcategory(self, queryset, name, value):
        return queryset.filter(Q(subcategory__label__iexact=value) | Q(subcategory__slug__iexact=value))

    def filter_discounted(self, queryset, name, value):
        if value:
            return queryset.filter(sale_price__isnull=False)
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        attributes = self.request.query_params.getlist("attributes")
        if attributes:
            for attribute in attributes:
                if ":" in attribute:
                    key, value = attribute.split(":", 1)
                    queryset = queryset.filter(attributes__name=key, attributes__value=value)
            queryset = queryset.distinct()
        return queryset


class ProductOrderingFilter(OrderingFilter):
    ordering_param = "sort"

    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)
        if ordering:
            return ordering
        sort = request.query_params.get(self.ordering_param)
        mapping = {
            "price-asc": ("price",),
            "price-desc": ("-price",),
            "newest": ("-created_at",),
        }
        return mapping.get(sort)


class ProductListAPIView(ListAPIView):
    serializer_class = CatalogProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, ProductOrderingFilter)
    filterset_class = ProductFilterSet
    search_fields = ("title", "description")
    ordering_fields = ("price", "created_at")

    def get_queryset(self):
        return (
            Product.objects.filter(is_active=True)
            .select_related("category", "subcategory")
            .prefetch_related("attributes", "media")
        )


class ProductDetailAPIView(RetrieveAPIView):
    queryset = (
        Product.objects.filter(is_active=True)
        .select_related("category", "subcategory")
        .prefetch_related("variants", "attributes", "media")
    )
    serializer_class = CatalogProductDetailSerializer
