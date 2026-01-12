from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


from janadesh.api.router import router
from .admin_views import filehub_embed

# Force router registrations
import blogs.api.v1.urls
import contacts.api.v1.urls
import galleries.api.v1.urls
import timelines.api.v1.urls
import newsletters.api.v1.urls
import campaign.api.v1.urls
import organization.api.v1.urls
import services.api.v1.urls
import menu.api.v1.urls
import analytics.api.v1.urls
import timelines.api.v1.urls


# ------------------------------------------------------------------------------
# Main URL patterns
# ------------------------------------------------------------------------------
urlpatterns = [
    # Admin & internal tools
    path("admin/", admin.site.urls),
    path("filemanager/", filehub_embed, name="admin_filehub"),

    # Web apps
    path("", include("filehub.urls")),
    path("analytics/", include("analytics.urls")),
    # path("campaign/", include("campaign.api.v1.urls")),
    path("menu/", include("menu.urls")),
    path("organization/", include("organization.urls")),
    path("seo/", include("seo.urls")),
    # path("services/", include("services.urls")),

    # Authentication (JWT)
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API v1 (ALL ViewSets from all apps)
    path("api/v1/", include(router.urls)),

    # DRF browsable API auth
    path("api-auth/", include("rest_framework.urls")),

    # OpenAPI schema & documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]


# ------------------------------------------------------------------------------
# Static & Media files (development only)
# ------------------------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# ------------------------------------------------------------------------------
# Static & Media files (development only)
# ------------------------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularSwaggerView,
#     SpectacularRedocView,
# )

# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from .admin_views import filehub_embed
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,  # login and get token
#     TokenRefreshView,
# )

# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()

# urlpatterns = [
#     path("filemanager/", filehub_embed, name="admin_filehub"),
#     path("", include("filehub.urls")),

#     path("admin/", admin.site.urls),
#     path("analytics/", include("analytics.urls")),
#     # path("api/<str:version>/blogs/", include("blogs.urls")),
#     path("campaign/", include("campaign.urls")),
#     # path("contacts/", include("contacts.urls")),
#     # path("galleries/", include("galleries.urls")),
#     path("menu/", include("menu.urls")),
#     path("organization/", include("organization.urls")),
#     path("seo/", include("seo.urls")),
#     path("services/", include("services.urls")),
#     # path("timelines/", include("timelines.urls")),
#     # path("newsletters/", include("newsletters.urls")),
#     path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
#     path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
#     # ----- API (versioned) -----
#     path("api/v1/blogs/", include("blogs.api.v1.urls")),
#     # path("api/v2/blogs/",?W include("blogs.api.v2.urls")),
    
#     path("api/v1/contacts/", include("contacts.api.v1.urls")),
    
#     # Example: Gallery API v1
#     path("api/v1/galleries/", include("galleries.api.v1.urls")),
    
#     # Example: Gallery API v1
#     path("api/v1/timelines/", include("timelines.api.v1.urls")),
#     path("api/v1/newsletters/", include("newsletters.api.v1.urls")),

    
#     # Optional: Django REST Framework browsable API authentication
#     path("api-auth/", include("rest_framework.urls")),
#     # path("tinymce/", include("tinymce.urls")),
#     # OpenAPI schema
#     path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
#     # Swagger UI
#     path(
#         "api/docs/",
#         SpectacularSwaggerView.as_view(url_name="schema"),
#         name="swagger-ui",
#     ),
#     # Redoc UI
#     path(
#         "api/redoc/",
#         SpectacularRedocView.as_view(url_name="schema"),
#         name="redoc",
#     ),
#     path("api/v1/", include(router.urls)),

# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

