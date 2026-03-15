from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class UserTypeMixin(LoginRequiredMixin):
    """
    Mixin for class-based views that restricts access to users with a
    specific user_type on their profile.

    Set ``required_user_type`` on the view class to the expected value
    (e.g. "tutor", "student", "app_admin", "content_admin").
    """

    required_user_type = None

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        # If LoginRequiredMixin already redirected, return that response
        if not request.user.is_authenticated:
            return response

        if self.required_user_type is not None:
            if not hasattr(request.user, "profile"):
                raise PermissionDenied
            if request.user.profile.user_type != self.required_user_type:
                raise PermissionDenied

        return response
