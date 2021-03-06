from django.conf.urls import patterns, include, url
from taxy.views import *
from django.contrib import admin
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'taxy.views.home', name='home'),
    # url(r'^taxy/', include('taxy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', root),
    url(r'^location_post/',location_post),
    url(r'^confirmation_post/',confirm_post),
    url(r'^trip_post/', trip_post),
    url(r'^customer_confirm/', customer_confirm),
)
