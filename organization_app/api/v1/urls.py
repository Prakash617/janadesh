from janadesh.api.router import router
from .views import (
    OrganizationViewSet,
)


# Register all routes with the shared router
router.register(r'organizations', OrganizationViewSet, basename='organization')


