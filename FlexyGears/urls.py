# coding: utf-8
from django.conf.urls import patterns, include, url
import os

site_media = os.path.join(os.path.dirname(__file__), '../site_media')

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'FlexyGears.views.home', name='home'),
    # url(r'^FlexyGears/', include('FlexyGears.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('userena.urls')),
    url(r'^$', 'FlexyGears.views.home'),

    # 开发服务器中提供的静态文件访问服务。生产环境中需要禁止以避免引起性能问题
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media}),
)
