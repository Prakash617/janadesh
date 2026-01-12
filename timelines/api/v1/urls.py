
from janadesh.api.router import router
from .views import TimelineViewSet



router.register(r'timeline', TimelineViewSet, basename='timeline')

