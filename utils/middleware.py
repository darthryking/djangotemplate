from django.utils import timezone
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from django.contrib.auth import logout

from djangotemplate.views import BanHammerLandingPage


class BanHammerMiddleware(object):
    def process_request(self, request):
        try:
            user = request.user
        except AttributeError:
            return None
            
        if user.is_authenticated() and not user.is_active:
            if request.get_full_path() != reverse('banhammer_landing'):
                logout(request)
                
                response = redirect('banhammer_landing')
                response.set_cookie(BanHammerLandingPage.cookieName, True)
                
                return response
                
        return None
        
        
class TimeZoneMiddleware(object):
    def process_request(self, request):
        try:
            user = request.user
        except AttributeError:
            return None
            
        if user.is_authenticated():
            timezone.activate(user.userprofile.timezone)
        else:
            timezone.deactivate()
            
        return None
        
        