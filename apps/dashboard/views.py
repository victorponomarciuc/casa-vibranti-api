from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib import admin

from apps.dashboard.services import get_dashboard_context


@staff_member_required
def dashboard_view(request):
    context = {
        **admin.site.each_context(request),
        "app_list": admin.site.get_app_list(request),
        "admin_dashboard": get_dashboard_context(),
    }
    return render(request, "admin/dashboard.html", context)
