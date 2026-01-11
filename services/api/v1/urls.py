from janadesh.api.router import router
from .views import ServiceViewSet




router.register("services", ServiceViewSet, basename="service")

