
from janadesh.api.router import router
from .views import ManifestoViewSet


router.register(r'manifesto', ManifestoViewSet, basename='manifeso')  # /api/v1/galleries/

