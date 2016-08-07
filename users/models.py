from __future__ import unicode_literals

from django.conf import settings

from django.db import models
from django.contrib.auth.models import User

import pytz


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    TIMEZONE_CHOICES = tuple(
        (timezone,) * 2
        for timezone in pytz.all_timezones
    )
    
    timezone = models.CharField(
        default=settings.TIME_ZONE,
        max_length=50,
        choices=TIMEZONE_CHOICES,
    )
    
    about = models.TextField(blank=True)
    
    class GenderChoices:
        MALE = 'M'
        FEMALE = 'F'
        OTHER = 'O'
        
    GENDER_CHOICES = (
        (GenderChoices.MALE, 'Male'),
        (GenderChoices.FEMALE, 'Female'),
        (GenderChoices.OTHER, 'Other'),
    )
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    def __unicode__(self):
        return "Profile for User '{}'".format(self.user.username)
        
        