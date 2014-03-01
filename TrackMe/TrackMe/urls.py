# project wide urls
from django.conf.urls import patterns, include, url
#from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from django.contrib import admin
admin.autodiscover()
import settings
from django.conf.urls.static import static

from django.views.generic import RedirectView


# import your urls from each app here, as needed
import trackapp.urls

urlpatterns = patterns('',

    # urls specific to this app
    url(r'^trackapp/', include(trackapp.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
 
   
    # catch all, redirect to trackapp home view
#    url(r'.*', RedirectView.as_view(url='/trackapp/home'))

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
