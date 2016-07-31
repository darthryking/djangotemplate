from django.conf.urls import include, url
from django.contrib import admin

from users import views

urlpatterns = (
    url(
        r'^login/$',
        views.LoginPage.as_view(),
        name='users_login',
    ),
    
    url(
        r'^register/$',
        views.RegisterPage.as_view(),
        name='users_register',
    ),
    
    url(
        r'^logout/$',
        views.LogoutPage.as_view(),
        name='users_logout',
    ),
    
    url(
        r'^profile/(?P<username>\w+)/$',
        views.ProfilePage.as_view(),
        name='users_profile',
    ),
    
    url(
        r'^settings/$',
        views.SettingsPage.as_view(),
        name='users_settings',
    ),
    
)
