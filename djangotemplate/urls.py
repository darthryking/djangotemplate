from django.conf.urls import patterns, include, url
from django.contrib import admin

from djangotemplate import views

handler403 = views.PermissionDeniedView.as_view()
handler404 = views.NotFoundView.as_view()
handler500 = views.ErrorView.as_view()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djangotemplate.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', views.IndexPage.as_view(), name='index'),
    
    url(r'^test/', include('testapp.urls')),
    url(r'^users/', include('users.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
)
