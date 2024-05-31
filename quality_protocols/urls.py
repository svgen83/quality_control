"""
URL configuration for quality_protocols project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path, include
from django.contrib.staticfiles.urls import static
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as authViews
from rabies_immunglobulin import views

urlpatterns = [
##    re_path(r'^horse/(?P<id>\d+)/$', views.horse, name='horse')
    re_path(r'^quality_protocol/(?P<title>\w+)/$',
            views.get_batch_protocol, name='quality_protocol'),
    path('admin/', admin.site.urls),
##    path('chaining/', include('smart_selects.urls')),
    path('', views.index, name='index'),
    path('batches', views.get_batches, name='batches'),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
