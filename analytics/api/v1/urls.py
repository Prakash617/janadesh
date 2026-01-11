from janadesh.api.router import router

from .views import (
    AnalyticsEventViewSet,
)


# Analytics
router.register("analytics", AnalyticsEventViewSet, basename="analytics")