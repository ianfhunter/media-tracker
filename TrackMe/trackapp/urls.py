# app specific urls
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^home', 'trackapp.views.home'),
    url(r'^search$', 'trackapp.views.search'),
    url(r'^item/(?P<value>\d+)$', 'trackapp.views.item'),
    url(r'^user/(?P<value>\d+)$', 'trackapp.views.user'),
    url(r'^login/$', 'trackapp.views.login'),
)
