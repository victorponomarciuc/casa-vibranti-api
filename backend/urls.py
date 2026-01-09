from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


admin.site.site_header = 'Casa Vibranti Admin'
admin.site.index_title = 'Casa Vibranti Admin'
admin.site.site_title = 'Casa Vibranti Admin Panel'
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('common/', include("apps.common.urls")),

]
urlpatterns += i18n_patterns(
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    path('admin/', admin.site.urls),

    prefix_default_language=False

)
if settings.DEBUG:
    urlpatterns += [
        path(
            "api/swagger/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)