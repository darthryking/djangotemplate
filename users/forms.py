from django.conf import settings

from django import forms
from django.contrib.auth.models import User

from users.models import UserProfile

from utils.decorators import html5_required
from utils.functions import get_field


def username_validator(username):
    if User.objects.filter(username__iexact=username).exists():
        raise forms.ValidationError("Username already exists!")
        
        
@html5_required
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=get_field(User, 'username').max_length,
    )
    password = forms.CharField(
        max_length=4096,
        widget=forms.PasswordInput(),
    )
    
    
@html5_required
class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=get_field(User, 'username').max_length,
        validators=[username_validator],
    )
    email = forms.EmailField()
    
    first_name = forms.CharField(
        label="First Name",
        max_length=get_field(User, 'first_name').max_length,
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=get_field(User, 'last_name').max_length,
    )
    
    password1 = forms.CharField(
        label="Password",
        max_length=4096,
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label="Password (Again)",
        max_length=4096,
        widget=forms.PasswordInput(),
    )
    
    timezone = forms.ChoiceField(
        initial=get_field(UserProfile, 'timezone').default,
        choices=get_field(UserProfile, 'timezone').choices,
    )
    gender = forms.ChoiceField(
        choices=get_field(UserProfile, 'gender').choices,
    )
    
    def clean(self):
        super(RegisterForm, self).clean()
        
        password1 = self.cleaned_data['password1']
        if password1 != self.cleaned_data['password2']:
            self.add_error('password1', "Passwords don't match!")
            
            
@html5_required
class SettingsForm(forms.Form):
    username = forms.CharField(
        max_length=get_field(User, 'username').max_length,
    )
    email = forms.EmailField()
    
    first_name = forms.CharField(
        label="First Name",
        max_length=get_field(User, 'first_name').max_length,
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=get_field(User, 'last_name').max_length,
    )
    
    timezone = forms.ChoiceField(
        choices=get_field(UserProfile, 'timezone').choices,
    )
    gender = forms.ChoiceField(
        choices=get_field(UserProfile, 'gender').choices,
    )
    
    about = forms.CharField(
        label="About Me",
        required=False,
        widget=forms.Textarea(),
    )
    
    password = forms.CharField(
        max_length=4096,
        required=False,
        widget=forms.PasswordInput(),
    )
    new_password1 = forms.CharField(
        label="New Password",
        max_length=4096,
        required=False,
        widget=forms.PasswordInput(),
    )
    new_password2 = forms.CharField(
        label="New Password (Again)",
        max_length=4096,
        required=False,
        widget=forms.PasswordInput(),
    )
    
    user = None
    
    def clean(self):
        super(SettingsForm, self).clean()
        
        password = self.cleaned_data['password']
        newPassword1 = self.cleaned_data['new_password1']
        newPassword2 = self.cleaned_data['new_password2']
        
        if password or newPassword1 or newPassword2:
            assert self.user is not None
            
            # Incorrect password
            if not self.user.check_password(password):
                self.add_error('password', "Password incorrect!")
                
            # Empty new password
            if not newPassword1:
                self.add_error(
                    'new_password1',
                    "New password cannot be empty!",
                )
                
            # Passwords don't match
            if newPassword1 != newPassword2:
                self.add_error('new_password1', "Passwords don't match!")
                
    def clean_username(self):
        username = self.cleaned_data['username']
        
        if (username != self.user.username
                and User.objects.filter(username__iexact=username).exists()):
            raise forms.ValidationError("Username already exists!")
            
        return username
        
        