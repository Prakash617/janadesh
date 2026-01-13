from .views import PageViewSet


router.register(r'pages', PageViewSet, basename='page')
