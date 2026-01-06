"""
URL configuration for janadesh project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analytics/', include('analytics.urls')),
    path('blogs/', include('blogs.urls')),
    path('campaign/', include('campaign.urls')),
    path('contacts/', include('contacts.urls')),
    path('galleries/', include('galleries.urls')),
    path('menu/', include('menu.urls')),
    path('organization/', include('organization.urls')),
    path('seo/', include('seo.urls')),
    path('services/', include('services.urls')),
    path('timelines/', include('timelines.urls')),
    path('newsletters/', include('newsletters.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
