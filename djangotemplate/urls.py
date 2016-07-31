"""djangotemplate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from djangotemplate import views

# Override the Admin Site header
admin.site.site_header = "djangotemplate Administration"

# Set the error handler views.
handler500 = views.ErrorHandler.as_view()
handler400 = views.Error400Handler.as_view()
handler403 = views.Error403Handler.as_view()
handler404 = views.Error404Handler.as_view()

urlpatterns = (
    url(r'^$', views.IndexPage.as_view(), name='index'),
    
    url(
        r'^logoutlanding/$',
        views.LogoutLandingPage.as_view(),
        name='logout_landing',
    ),
    
    url(
        r'^accountdisabledlanding/$',
        views.BanHammerLandingPage.as_view(),
        name='banhammer_landing',
    ),
    
    url(
        r'^maintenancelanding/$',
        views.MaintenanceLandingPage.as_view(),
        name='maintenance_landing',
    ),
    
    url(r'^admin/', admin.site.urls),
    
    url(r'^users/', include('users.urls')),
    url(r'^test/', include('testapp.urls')),
)
