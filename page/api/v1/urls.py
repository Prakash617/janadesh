from janadesh.api.router import router
from .views import *



router.register(r'pages', PageViewSet, basename='page')


