from . import views
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import User, Doctor, Patient, Patient_file, Patient_Visit, Patient_Vitals

def doctor_required(view_func):

    @wraps(view_func)

    def _wrapped_view(request,*args,**kwargs):

        if not request.user.is_authenticated or request.user.user_type != 'doctor':
            raise PermissionDenied

        return view_func(request,*args,**kwargs)

    return _wrapped_view