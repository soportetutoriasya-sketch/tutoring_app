from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def user_type_required(user_type):
    """
    Decorator that checks if the authenticated user's profile has the
    specified user_type. Raises PermissionDenied (403) if not.
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, "profile"):
                raise PermissionDenied
            if request.user.profile.user_type != user_type:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


student_required = user_type_required("student")
tutor_required = user_type_required("tutor")
admin_required = user_type_required("app_admin")
