from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import patterns, include, url

from testapp import views


urlpatterns = patterns('',
    url(
            r'^echo/$',
            login_required(views.EchoView.as_view()),
            name='test_echo',
        ),
        
    url(
            r'^500/$',
            login_required(views.Generate500View.as_view()),
            name='test_500',
        ),
        
    url(
            r'^403/$',
            login_required(views.Generate403View.as_view()),
            name='test_403',
        ),
        
)

