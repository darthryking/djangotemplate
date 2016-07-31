from django.conf import settings

from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import pytz

from users.models import UserProfile

from djangotemplate.views import LogoutLandingPage


class LoginPage(View):
    template_name = 'users/login.html'
    
    def get(self, request):
        getData = request.GET
        
        context = {}
        
        if 'next' in getData:
            context['next'] = getData['next']
            
        return render(request, self.template_name, context)
    
    def post(self, request):
        postData = request.POST
        
        try:
            username = postData['username']
            password = postData['password']
        except KeyError:
            return HttpResponseBadRequest("Bad Request!")
            
        userQuery = User.objects.filter(username__iexact=username)
        
        if userQuery.exists():
            assert userQuery.count() == 1
            username = userQuery[0].username
            
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                
                # Everything is OK
                if 'next' in postData:
                    return redirect(postData['next'])
                else:
                    return redirect('users_profile', username=username)
                    
            else:
                # Account Disabled
                messages.error(
                    request,
                    "Your account has been disabled. If this is unexpected, "
                    "please contact the site administrators for help.",
                )
                return redirect(request.get_full_path())
                
        else:
            # Authentication Failed
            messages.error(request, "Login failed!")
            return redirect(request.get_full_path())
            
            
class RegisterPage(View):
    template_name = 'users/register.html'
    
    def get(self, request):
        getData = request.GET
        
        context = {
            'timezones'         :   pytz.all_timezones,
            'GENDER_CHOICES'    :   UserProfile.GENDER_CHOICES,
        }
        
        if 'next' in getData:
            context['next'] = getData['next']
            
        return render(request, self.template_name, context)
        
    def post(self, request):
        postData = request.POST
        
        try:
            username = postData['username'].strip()
            email = postData['email'].strip()
            firstName = postData['firstname'].strip()
            lastName = postData['lastname'].strip()
            password1 = postData['password1']
            password2 = postData['password2']
            timezone = postData['timezone']
            gender = postData['gender']
            
        except KeyError:
            return HttpResponseBadRequest("Bad Request!")
            
        # Username, email, names, and password cannot be blank.
        if not all((username, email, firstName, lastName, password1)):
            return HttpResponseBadRequest("Bad Request!")
            
        # Timezone must be valid.
        if timezone not in pytz.all_timezones:
            timezone = settings.TIME_ZONE
            
        # Gender must be valid.
        if gender not in (choice[0] for choice in UserProfile.GENDER_CHOICES):
            gender, _ = UserProfile.GENDER_CHOICES[0]
            
        # Username must not already exist.
        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username already exists!")
            return redirect(request.get_full_path())
            
        # Passwords must match.
        if password1 != password2:
            messages.error(request, "Passwords don't match!")
            return redirect(request.get_fill_path())
            
        with transaction.atomic():
            newUser = User.objects.create_user(
                username=username,
                password=password1,
                email=email,
                first_name=firstName,
                last_name=lastName,
            )
            
            newProfile = UserProfile(
                user=newUser,
                timezone=timezone,
                gender=gender,
            )
            newProfile.save()
            
        user = authenticate(username=username, password=password1)
        login(request, user)
        
        if 'next' in postData:
            return redirect(postData['next'])
        else:
            return redirect('users_profile', username=username)
            
            
class LogoutPage(View):
    def get(self, request):
        logout(request)
        
        response = redirect('logout_landing')
        response.set_cookie(LogoutLandingPage.cookieName, True)
        
        return response
        
        
class ProfilePage(View):
    template_name = 'users/profile.html'
    
    def get(self, request, username=None):
        assert username is not None
        
        user = get_object_or_404(User, username__iexact=username)
        
        context = {
            'profileuser'   :   user,
        }
        
        return render(request, self.template_name, context)
        
        
class SettingsPage(View):
    template_name = 'users/settings.html'
    
    @method_decorator(login_required)
    def dispatch(self, request):
        return super(SettingsPage, self).dispatch(request)
        
    def get(self, request):
        context = {
            'timezones'         :   pytz.all_timezones,
            'GENDER_CHOICES'    :   UserProfile.GENDER_CHOICES,
        }
        
        return render(request, self.template_name, context)
        
    def post(self, request):
        postData = request.POST
        
        try:
            username = postData['username'].strip()
            email = postData['email'].strip()
            firstName = postData['firstname'].strip()
            lastName = postData['lastname'].strip()
            timezone = postData['timezone']
            gender = postData['gender']
            about = postData['about']
            password = postData['password']
            newPassword1 = postData['newpassword1']
            newPassword2 = postData['newpassword2']
            
        except KeyError:
            return HttpResponseBadRequest("Bad Request!")
            
        # Username must not be blank.
        if not username:
            username = request.user.username
            
        # Email must not be blank.
        if not email:
            email = request.user.email
            
        # First name must not be blank.
        if not firstName:
            firstName = request.user.first_name
            
        # Last name must not be blank.
        if not lastName:
            lastName = request.user.last_name
            
        # New username must not already exist.
        if (username != request.user.username
                and User.objects.filter(username__iexact=username).exists()):
            messages.error("Username already exists!")
            return redirect(request.get_full_path())
            
        # Timezone must be valid.
        if timezone not in pytz.all_timezones:
            timezone = settings.TIME_ZONE
            
        # Gender must be valid.
        if gender not in (choice[0] for choice in UserProfile.GENDER_CHOICES):
            gender, _ = UserProfile.GENDER_CHOICES[0]
            
        with transaction.atomic():
            user = request.user
            
            if password or newPassword1 or newPassword2:
                # Incorrect password
                if not user.check_password(password):
                    messages.error(request, "Password incorrect!")
                    return redirect(request.get_full_path())
                    
                # Empty new password
                if not newPassword1:
                    messages.error(request, "New password cannot be empty!")
                    return redirect(request.get_full_path())
                    
                # Passwords don't match
                if newPassword1 != newPassword2:
                    messages.error(request, "Passwords don't match!")
                    return redirect(request.get_full_path())
                    
                user.set_password(newPassword1)
                user.save()
                
                user = authenticate(
                    username=user.username,
                    password=newPassword1,
                )
                
                assert user is not None
                
                login(request, user)
                
            userProfile = user.userprofile
            
            user.username = username
            user.email = email
            user.first_name = firstName
            user.last_name = lastName
            
            userProfile.timezone = timezone
            userProfile.about = about
            userProfile.gender = gender
            
            user.save()
            userProfile.save()
            
        return redirect('users_profile', username=username)
        
        