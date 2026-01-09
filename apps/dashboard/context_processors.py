from apps.dashboard.services import get_dashboard_context


def admin_dashboard(request):
    match = getattr(request, "resolver_match", None)
    if not match or match.app_name != "admin" or match.url_name != "index":
        return {}
    return {"admin_dashboard": get_dashboard_context()}
