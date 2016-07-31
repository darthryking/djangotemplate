from django.http import HttpResponse
from django.views.generic import View
from django.core.exceptions import PermissionDenied

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from utils.decorators import staff_only


class EchoView(View):
    """ Test View for echoing GET and POST request data. """
    
    def get(self, request):
        response = '\n'.join(
            ('='.join(pair) for pair in request.GET.iteritems())
        )
        return HttpResponse(response)
        
    def post(self, request):
        response = '\n'.join(
            ('='.join(pair) for pair in request.POST.iteritems())
        )
        return HttpResponse(response)
        
        
class LoginCheckView(View):
    """ Test View that displays which user is currently logged in. """
    def get(self, request):
        return HttpResponse(str(request.user))
        
        
class StaffOnlyView(View):
    """ Test View that checks if the user is a staff user. """
    
    @method_decorator(staff_only)
    def get(self, request):
        return HttpResponse("Staff only!")
        
        
class Generate403View(View):
    """ Test View for generating an HTTP 403. """
    
    def get(self, request):
        raise PermissionDenied
        
        
class Generate500View(View):
    """ Test View for generating an HTTP 500. """
    
    def get(self, request):
        raise Exception("Generated Test Exception")
        
        