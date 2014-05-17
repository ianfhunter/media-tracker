# app specific urls
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^home', 'trackapp.views.home'),
    url(r'^search$', 'trackapp.views.search'),
    url(r'^item/(?P<value>\w+)$', 'trackapp.views.item'),
    url(r'^item/(?P<value>\w+)/status_update/$', 'trackapp.views.status_update'),
    url(r'^user/(?P<value>\w+)$', 'trackapp.views.user'),
    url(r'^login/$', 'trackapp.views.login'),
    url(r'^/?$', 'trackapp.views.home'),
)
