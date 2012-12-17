from django.conf.urls import patterns, include, url
#from cscm.views import current_datetime 
from cscm.views.reports_list import *
from cscm.views.report_nceac_courselog import *
from cscm.views.report_qec_courselog import *    
from cscm.views.report_nceac_coursedesc import * 
from csip.views.report_nceac_faculty_profile import *

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
    # url(r'^helloview', make_hello_report),
    url(r'^reports/all', display_complete_report_list),
    url(r'^reports/nceac/courselog', report_nceac_courselog), 
    url(r'^reports/qec/courselog', report_qec_courselog), 
    url(r'^reports/nceac/coursedesc', report_nceac_coursedesc),
    url(r'^reports/nceac/faculty-profile', report_nceac_faculty_profile),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^grappelli/', include('grappelli.urls')),
)


