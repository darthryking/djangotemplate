from django.conf.urls import include, url
from django.contrib import admin

from testapp import views

urlpatterns = (
    url(
        r'^echo/$',
        views.EchoView.as_view(),
        name='test_echo',
    ),
    
    url(
        r'^logincheck/$',
        views.LoginCheckView.as_view(),
        name='test_logincheck',
    ),
    
    url(
        r'^staffonly/$',
        views.StaffOnlyView.as_view(),
        name='test_staffonly',
    ),
    
    url(
        r'^500/$',
        views.Generate500View.as_view(),
        name='test_500',
    ),
    
    url(
        r'^403/$',
        views.Generate403View.as_view(),
        name='test_403',
    ),
    
)
