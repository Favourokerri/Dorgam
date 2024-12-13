from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages

def is_logged_in(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            if not request.user.is_authenticated:
                messages.warning(request, "please login to continue")
                return redirect('login')
            return func(request, *args, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
            return redirect('login')
    return wrapper
