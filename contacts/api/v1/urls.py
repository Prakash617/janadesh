from django.urls import path, include
from janadesh.api.router import router
from contacts.api.v1.views import ContactViewSet

app_name = 'contacts-api-v1'



router.register("contacts", ContactViewSet, basename="contact")


