import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.categories.models import Category, Subcategory


class ProductKind(models.TextChoices):
    IMAGE = "image", _("Image")
    VIDEO = "video", _("Video")
    AD = "ad", _("Ad")


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kind = models.CharField(max_length=8, choices=ProductKind.choices, default=ProductKind.IMAGE)
    title = models.CharField(max_length=180)
    description = models.TextField()
    price = models.PositiveIntegerField()
    sale_price = models.PositiveIntegerField(null=True, blank=True)
    cta = models.CharField(max_length=60, blank=True)
    tags = models.JSONField(default=list, blank=True)
    media_src = models.URLField(blank=True)
    poster = models.URLField(blank=True)
    href = models.URLField(blank=True)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, related_name="products", on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

    def primary_media(self):
        return self.media.order_by("sort_order").first()

    def attributes_as_dict(self) -> dict:
        return {item.name: item.value for item in self.attributes.order_by("sort_order")}


class ProductMedia(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image", _("Image")
        VIDEO = "video", _("Video")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, related_name="media", on_delete=models.CASCADE)
    media_type = models.CharField(max_length=8, choices=MediaType.choices, default=MediaType.IMAGE)
    file = models.FileField(upload_to="products/media/", blank=True)
    external_url = models.URLField(blank=True)
    poster = models.FileField(upload_to="products/posters/", blank=True)
    alt_text = models.CharField(max_length=120, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self) -> str:
        return f"{self.product.title} ({self.media_type})"

    def media_url(self) -> str:
        if self.external_url:
            return self.external_url
        if self.file:
            return self.file.url
        return ""

    def poster_url(self) -> str:
        if self.poster:
            return self.poster.url
        return ""


class ProductVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=40)
    color_swatch = models.CharField(max_length=32, blank=True)
    sku = models.CharField(max_length=40, unique=True)
    price_override = models.PositiveIntegerField(null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self) -> str:
        return f"{self.product.title} - {self.size}/{self.color}"


class ProductAttribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, related_name="attributes", on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    value = models.CharField(max_length=120)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self) -> str:
        return f"{self.name}: {self.value}"


class ProductMetrics(models.Model):
    product = models.OneToOneField(Product, related_name="metrics", on_delete=models.CASCADE)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.product.title} metrics"
