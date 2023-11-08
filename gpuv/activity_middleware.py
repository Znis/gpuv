from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime,timedelta
from django.http import JsonResponse


class ActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)


        if request.path == '/check-session/':
            if not request.session.get('last_active_time'):
                # Set the initial value for the last active time
            
                request.session['last_active_time'] = datetime.now().isoformat()
            else:
                last_active_time = datetime.fromisoformat(request.session['last_active_time'])
                current_time = datetime.now()

                if current_time > last_active_time + timedelta(seconds=5):
                    # Session has expired, send response to the frontend
                    request.session.flush()
                    return JsonResponse({'message': 'Session expired'}, status=401)
                

                # Update the last active time
                request.session['last_active_time'] = current_time.isoformat()

        return response