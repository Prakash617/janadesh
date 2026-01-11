from django.urls import path, include
from janadesh.api.router import router
from .views import GalleryViewSet

app_name = 'galleries-api-v1'

# -----------------------------
# Router
# -----------------------------
router.register(r'gallaries', GalleryViewSet, basename='galleries')  # /api/v1/galleries/

# -----------------------------

