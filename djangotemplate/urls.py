from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from djangotemplate import views

handler403 = views.PermissionDeniedView.as_view()
handler404 = views.NotFoundView.as_view()
handler500 = views.ErrorView.as_view()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djangotemplate.views.home', name='home'),
    # url(r'^djangotemplate/', include('djangotemplate.foo.urls')),
    
    url(r'^$', views.IndexPage.as_view(), name='index'),
    
    url(r'^users/', include('users.urls')),
    url(r'^test/', include('testapp.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

