from functools import partial

from django.contrib.auth.models import User
from users.models import UserProfile


def get_field(Model, field):
    return Model._meta.get_field(field)
    
    
def field_arg(Model, field, arg):
    return getattr(Model._meta.get_field(field), arg)
    
    
def field_len(Model, field):
    """ Given a Model and a field name, returns the max length of the field.
    """
    
    return field_arg(Model, field, 'max_length')
    
    
def field_default(Model, field):
    """ Given a Model and a field name, returns the default value of the field.
    """
    
    return field_arg(Model, field, 'default')
    
    
def field_choices(Model, field):
    """ Given a Model and a field name, returns the field's choices. """
    return field_arg(Model, field, 'choices')
    
    