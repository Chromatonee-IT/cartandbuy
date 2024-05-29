from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path as url
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap
from .sitemaps import *

sitemaps= {
    'static': StaticSitemap,
    'categories':CategorySitemap,
    'subcategory':SubcategorySitemap,
    'products':ProductsSitemap
}

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root':settings.STATIC_ROOT}),
    path('sitemap.xml',sitemap,{'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    path('',include('store.urls')),
    path('',include('vendor.urls')),
    path('',include('django.contrib.auth.urls')),
]
urlpatterns += static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
