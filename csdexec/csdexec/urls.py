from django.conf.urls import patterns, include, url
#from cscm.views import current_datetime 
from cscm.views.test import make_hello_report

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'csdexec.views.home', name='home'),
    # url(r'^csdexec/', include('csdexec.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include(admin.site.urls)),
    # url(r'^helloview', current_datetime)
    url(r'^helloview', make_hello_report)
)


