from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.utils import timezone

from apps.orders.models import Order, OrderItem
from apps.products.models import Product


@staff_member_required
def dashboard_view(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()

    start_date = timezone.now() - timedelta(days=365)
    orders_by_month = (
        Order.objects.filter(created_at__gte=start_date)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("total"))
        .order_by("month")
    )

    top_products = (
        OrderItem.objects.values("product__title")
        .annotate(quantity=Sum("quantity"))
        .order_by("-quantity")[:5]
    )

    most_viewed = (
        Product.objects.select_related("metrics")
        .order_by("-metrics__views_count")
        .values("title", "metrics__views_count")[:5]
    )

    most_sold = (
        OrderItem.objects.values("product__title")
        .annotate(quantity=Sum("quantity"))
        .order_by("-quantity")[:5]
    )

    context = {
        "total_products": total_products,
        "total_orders": total_orders,
        "orders_by_month": orders_by_month,
        "top_products": top_products,
        "most_viewed": most_viewed,
        "most_sold": most_sold,
    }
    return render(request, "admin/dashboard.html", context)
