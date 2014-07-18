# app specific urls
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^search$', 'trackapp.views.search'),
    url(r'^add_item', 'trackapp.views.item'),
    url(r'^do_add_item', 'trackapp.views.add_item'),
    url(r'^settings', 'trackapp.views.settings'),
    url(r'^stats', 'trackapp.views.stats'),
    url(r'^library', 'trackapp.views.library'),
    url(r'^/?', 'trackapp.views.home'),
)
