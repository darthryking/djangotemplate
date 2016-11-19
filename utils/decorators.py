"""

decorators.py

Miscellaneous decorators.

"""

try:
    import cPickle as pickle
except ImportError:
    import pickle
    
from functools import wraps

from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login


def memoized(f):
    """ Simple memoization decorator. """
    
    _cache = {}
    
    @wraps(f)
    def wrapper(*args, **kwargs):
        key = pickle.dumps((args, kwargs), 2)
        
        if key not in _cache:
            result = f(*args, **kwargs)
            _cache[key] = result
        else:
            result = _cache[key]
            
        return result
        
    return wrapper
    
    
def staff_only(view):
    """ Staff-only View decorator. """
    
    @wraps(view)
    def decorated_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path())
            
        if not request.user.is_staff:
            raise PermissionDenied
            
        return view(request, *args, **kwargs)
        
    return decorated_view
    
    
def html5_required(Form):
    """ Adds a "required" HTML5 attribute to any Form fields that are 
    required.
    
    """
    
    for fieldName, field in Form.base_fields.iteritems():
        if field.required:
            field.widget.attrs['required'] = 'required'
            
    return Form
    
    