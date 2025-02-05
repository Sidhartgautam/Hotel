from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Correct the variable name from `url_patterns` to `urlpatterns`
urlpatterns = [
    path('admin/', admin.site.urls),
    path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("docs/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path('api/', include('core.api_urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# If needed, you can add static files handling back:
# from django.conf import settings
# from django.conf.urls.static import static
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
#     settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
# )
