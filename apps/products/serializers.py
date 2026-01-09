from rest_framework import serializers

from apps.products.models import Product, ProductAttribute, ProductMedia, ProductVariant


class ProductVariantSerializer(serializers.ModelSerializer):
    colorSwatch = serializers.CharField(source="color_swatch")
    priceOverride = serializers.IntegerField(source="price_override", allow_null=True, required=False)

    class Meta:
        model = ProductVariant
        fields = ("id", "size", "color", "colorSwatch", "sku", "priceOverride")


class ProductMediaSerializer(serializers.ModelSerializer):
    mediaType = serializers.CharField(source="media_type")
    mediaSrc = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()
    altText = serializers.CharField(source="alt_text", allow_blank=True)
    isPrimary = serializers.BooleanField(source="is_primary")
    sortOrder = serializers.IntegerField(source="sort_order")

    class Meta:
        model = ProductMedia
        fields = ("id", "mediaType", "mediaSrc", "poster", "altText", "caption", "isPrimary", "sortOrder")

    def get_mediaSrc(self, obj: ProductMedia) -> str:
        return obj.media_url()

    def get_poster(self, obj: ProductMedia) -> str:
        return obj.poster_url()


class CatalogProductSerializer(serializers.ModelSerializer):
    salePrice = serializers.IntegerField(source="sale_price", allow_null=True, required=False)
    mediaSrc = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "kind",
            "title",
            "description",
            "price",
            "salePrice",
            "cta",
            "tags",
            "mediaSrc",
            "poster",
            "href",
            "category",
            "subcategory",
            "attributes",
        )

    def get_mediaSrc(self, obj: Product) -> str:
        primary = obj.media.filter(is_primary=True).order_by("sort_order").first() or obj.primary_media()
        if primary:
            return primary.media_url()
        return obj.media_src

    def get_poster(self, obj: Product) -> str:
        primary = obj.media.filter(is_primary=True).order_by("sort_order").first() or obj.primary_media()
        if primary:
            return primary.poster_url()
        return obj.poster

    def get_category(self, obj: Product) -> str:
        return obj.category.label

    def get_subcategory(self, obj: Product) -> str:
        return obj.subcategory.label

    def get_attributes(self, obj: Product) -> dict:
        return obj.attributes_as_dict()


class CatalogProductDetailSerializer(CatalogProductSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    media = ProductMediaSerializer(many=True, read_only=True)

    class Meta(CatalogProductSerializer.Meta):
        fields = CatalogProductSerializer.Meta.fields + ("variants", "media")
