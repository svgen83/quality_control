from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.staticfiles.urls import static
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as authViews
from rabies_immunglobulin import views
##from django.urls import path, register_converter
##from datetime import datetime




urlpatterns = [
    re_path(r'^quality_protocol/(?P<title>\w+)/$',
            views.get_batch_protocol, name='quality_protocol'),
    re_path(r'^method/(?P<pk>\d+)/$',
            views.get_method, name='method'),
    re_path(r'^batch_docs/(?P<title>\w+)/$',
            views.get_batch_docs,
            name='batch_docs'),
##    re_path(r'^standart_sample/(?P<title>\D+)/(?P<date>\d{4}-\d{2}-\d{2})/$',
##            views.get_standart_sample,
##            name='standart_sample'),
    re_path(r'^standart_sample/(?P<title>\D.+)/(?P<date>\d{4}-\d{2}-\d{2})/$',
            views.get_standart_sample,
            name='standart_sample'),

    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('batches', views.get_batches, name='batches'),
    path('graphs/', views.get_graphs, name='graphs'),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
