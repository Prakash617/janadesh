from django.urls import path, include
from janadesh.urls import router
from contacts.api.v1.views import ContactViewSet

app_name = 'contacts-api-v1'



router.register(r'', ContactViewSet, basename='contact')

urlpatterns = [
    path('', include(router.urls)),
]
