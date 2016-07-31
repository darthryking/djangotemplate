from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView


class IndexPage(TemplateView):
    template_name = 'index.html'
    
    
class LandingPage(View):
    """ Abstract base class for Landing Page views. """
    
    template_name = 'landing.html'
    
    status = 200
    
    def get(self, request):
        cookies = request.COOKIES
        
        if self.cookieName not in cookies:
            return redirect(self.redirectURL)
            
        context = {
            'title'     :   self.title,
            'message'   :   self.message,
        }
        
        response = render(
            request,
            self.template_name,
            context,
            status=self.status,
        )
        response.delete_cookie(self.cookieName)
        
        return response
        
        
class LogoutLandingPage(LandingPage):
    cookieName = 'LOGOUT_LANDING'
    
    title = "Logged Out"
    
    message = "You have been logged out. Thanks for stopping by!"
    
    redirectURL = 'index'
    
    
class BanHammerLandingPage(LandingPage):
    cookieName = 'BANHAMMER_LANDING'
    
    title = "Account Disabled"
    
    message = (
        "Your account has been disabled. If this is unexpected, please "
        "contact the site administrators for help."
    )
    
    redirectURL = 'index'
    
    
class MaintenanceLandingPage(LandingPage):
    cookieName = 'MAINTENANCE_LANDING'
    
    title = "Pardon Our Mess!"
    
    message = (
        "The site is currently undergoing routine maintenance, and is "
        "currently unavailable. Sorry about that! If you have any questions, "
        "feel free to contact the site administrators."
    )
    
    redirectURL = 'index'
    
    status = 503
    
    
class ErrorHandler(View):
    """ A view that handles errors. By itself, serves as an HTTP 500 handler.
    """
    
    template_name = 'error.html'
    
    errnum = 500
    
    title = "Internal Server Error"
    
    message = (
        "Whoops! Looks like we screwed something up. "
        "Don't worry; the site admins have been contacted, and they have "
        "dispatched a specially-trained team of code monkeys to clean up the "
        "mess. We'll get everything fixed for you soon!"
    )
    
    def get(self, request):
        
        context = {
            'title'     :   self.title,
            'errnum'    :   self.errnum,
            'message'   :   self.message,
        }
        
        return render(request, self.template_name, context, status=self.errnum)
        
    def post(self, request):
        return self.get(request)
        
        
class Error400Handler(ErrorHandler):
    """ A view that handles HTTP 400 Bad Request errors. """
    
    errnum = 400
    
    title = "Bad Request"
    
    message = (
        "Either you or your browser messed something up. If this persists "
        "and you have no idea why, please contact the site admins for help."
    )
    
    
class Error403Handler(ErrorHandler):
    """ A view that handles HTTP 403 Forbidden errors. """
    
    errnum = 403
    
    title = "Permission Denied"
    
    message = "You don't have permission to do that!"
    
    
class Error404Handler(ErrorHandler):
    """ A view that handles HTTP 404 Not Found errors. """
    
    errnum = 404
    
    title = "Not Found"
    
    message = (
        "This page doesn't exist. "
        "Are you sure the address is correct?"
    )
    
    