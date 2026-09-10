from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def login_required_user(view_func):
    """Decorator to enforce student/user login."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.warning(request, "Please log in to access this page.")
            return redirect('user_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_required(view_func):
    """Decorator to enforce administrator authentication and role."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        role = request.session.get('role')
        if not user_id or role != 'admin':
            messages.error(request, "Access denied. Administrator privileges required.")
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
