from django.conf.urls import patterns, include, url
#from cscm.views import current_datetime 
from cscm.views.reports_list import *
from cscm.views.main_menu import *
from cscm.views.report_nceac_courselog import *
from cscm.views.report_qec_courselog import *    
from cscm.views.report_qec_course_catalog import *
from cscm.views.report_qec_program_objectives import *  
from cscm.views.report_nceac_coursedesc import * 
from cscm.views.report_internal_courseoutline import * 
from csip.views.report_nceac_faculty_profile import *
from csip.views.report_internal_faculty_cv import *
from csip.views.report_qec_interest_areas import *
from csip.views.report_qec_list_publications import *
from csip.views.report_qec_faculty_profile import * 


from cspj.views.report_internal_prog_milestone import * 
from cspj.views.report_internal_prog_complete import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'csdexec.views.home', name='home'),
    # url(r'^csdexec/', include('csdexec.foo.urls')),

    url(r'^grappelli/', include('grappelli.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', display_main_menu),
    # url(r'^helloview', make_hello_report),
    url(r'^reports/all', display_complete_report_list),
    url(r'^reports/nceac/courselog', report_nceac_courselog),
    url(r'^reports/qec/courselog', report_qec_courselog),
    url(r'^reports/qec/coursecatalog', report_qec_course_catalog),
    url(r'^reports/qec/programobjectives', report_qec_program_objectives),
    url(r'^reports/qec/interestareas', report_qec_interest_areas),
    url(r'^reports/qec/publicationlist', report_qec_list_publications),
    url(r'^reports/qec/faculty-cv', report_qec_faculty_profile),
    url(r'^reports/nceac/coursedesc', report_nceac_coursedesc),
    url(r'^reports/nceac/faculty-profile', report_nceac_faculty_profile),
    url(r'^reports/internals/instructor-cv', report_internal_faculty_cv),
    url(r'^reports/internal/projects/milestone', report_internal_prog_milestone),
    url(r'^reports/internal/projects/complete', report_internal_prog_complete),
    url(r'^reports/internal/course/outline/(?P<type>[a-z]*)/', report_internal_courseoutline),
    url(r'^reports/internal/course/outline', report_internal_courseoutline),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
)


