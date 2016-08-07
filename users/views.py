from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from users.models import UserProfile
from users.forms import LoginForm, RegisterForm, SettingsForm

from djangotemplate.views import LogoutLandingPage


class LoginPage(View):
    template_name = 'users/login.html'
    
    def get(self, request):
        if request.user.is_authenticated():
            return redirect('index')
            
        getData = request.GET
        
        context = {
            'loginForm' :   LoginForm(),
        }
        
        if 'next' in getData:
            context['next'] = getData['next']
            
        return render(request, self.template_name, context)
        
    def post(self, request):
        if request.user.is_authenticated():
            return redirect('index')
            
        postData = request.POST
        
        loginForm = LoginForm(postData)
        
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            
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
                    loginForm.add_error(
                        None,
                        "Your account has been disabled. "
                        "If this is unexpected, please contact the site "
                        "administrators for help.",
                    )
                    
            else:
                # Authentication Failed
                loginForm.add_error(None, "Login failed!")
                
        context = {
            'loginForm' :   loginForm,
        }
        
        return render(request, self.template_name, context)
        
        
class RegisterPage(View):
    template_name = 'users/register.html'
    
    def get(self, request):
        if request.user.is_authenticated():
            return redirect('index')
            
        getData = request.GET
        
        context = {
            'regForm'   :   RegisterForm(),
        }
        
        if 'next' in getData:
            context['next'] = getData['next']
            
        return render(request, self.template_name, context)
        
    def post(self, request):
        if request.user.is_authenticated():
            return redirect('index')
            
        postData = request.POST
        
        regForm = RegisterForm(postData)
        
        if regForm.is_valid():
            cleanedData = regForm.cleaned_data
            
            username = cleanedData['username']
            email = cleanedData['email']
            password = cleanedData['password1']
            firstName = cleanedData['first_name']
            lastName = cleanedData['last_name']
            timezone = cleanedData['timezone']
            gender = cleanedData['gender']
            
            with transaction.atomic():
                newUser = User.objects.create_user(
                    username=username,
                    password=password,
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
                
            user = authenticate(username=username, password=password)
            login(request, user)
            
            if 'next' in postData:
                return redirect(postData['next'])
            else:
                return redirect('users_profile', username=username)
                
        else:
            context = {
                'regForm'   :   regForm,
            }
            
            return render(request, self.template_name, context)
            
            
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
        user = request.user
        userProfile = user.userprofile
        
        settingsForm = SettingsForm(
            initial={
                'username'      :   user.username,
                'email'         :   user.email,
                'first_name'    :   user.first_name,
                'last_name'     :   user.last_name,
                'timezone'      :   userProfile.timezone,
                'gender'        :   userProfile.gender,
                'about'         :   userProfile.about,
            },
        )
        
        context = {
            'settingsForm'  :   settingsForm,
        }
        
        return render(request, self.template_name, context)
        
    def post(self, request):
        postData = request.POST
        
        settingsForm = SettingsForm(postData)
        settingsForm.user = request.user
        
        if settingsForm.is_valid():
            cleanedData = settingsForm.cleaned_data
            
            username = cleanedData['username']
            email = cleanedData['email']
            firstName = cleanedData['first_name']
            lastName = cleanedData['last_name']
            timezone = cleanedData['timezone']
            gender = cleanedData['gender']
            about = cleanedData['about']
            password = cleanedData['password']
            newPassword1 = cleanedData['new_password1']
            newPassword2 = cleanedData['new_password2']
            
            with transaction.atomic():
                user = request.user
                
                if password or newPassword1 or newPassword2:
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
            
        else:
            context = {
                'settingsForm'  :   settingsForm,
            }
            
            return render(request, self.template_name, context)
            
            