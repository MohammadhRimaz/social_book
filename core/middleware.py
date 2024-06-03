from django.utils import timezone
from django.contrib.auth.middleware import get_user
from django.utils.deprecation import MiddlewareMixin
from .models import Profile

class UpdateLastSeenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user =get_user(request)
        if user.is_authenticated:
            Profile.objects.filter(user=user).update(last_seen=timezone.now())