from django.urls import path

from apps.products.views import ProductDetailAPIView, ProductListAPIView

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name="catalog-products"),
    path("products/<uuid:pk>/", ProductDetailAPIView.as_view(), name="catalog-product-detail"),
]
