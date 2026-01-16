from janadesh.api.router import router
from .views import AboutViewSet



router.register(r"website", AboutViewSet, basename="website")
