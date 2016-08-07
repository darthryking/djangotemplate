"""

functions.py

Miscellaneous helper functions.

"""

def get_field(Model, field):
    """ Given a Model and a field name, returns the corresponding field object.
    """
    return Model._meta.get_field(field)
    
    