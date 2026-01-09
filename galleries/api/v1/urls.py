from django.urls import path, include
from janadesh.urls import router
from .views import GalleryViewSet

app_name = 'galleries-api-v1'

# -----------------------------
# Router
# -----------------------------
router.register(r'', GalleryViewSet, basename='galleries')  # /api/v1/galleries/

# -----------------------------
# URL patterns
# -----------------------------
urlpatterns = [
    path('', include(router.urls)),
]
