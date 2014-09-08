from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    """ Override the Admin header. """
    
    site_header = 'Django Template Administration'
    
    
admin_site = CustomAdminSite()
