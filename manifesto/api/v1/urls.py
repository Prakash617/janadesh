
from janadesh.api.router import router
from .views import ManifestoViewSet


router.register(r'manifeso', ManifestoViewSet, basename='manifeso')  # /api/v1/galleries/

