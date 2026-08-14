from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .response_utils import success_response


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    base = request.build_absolute_uri('/').rstrip('/')
    return success_response('Task Management API is running', {
        'status': 'ok',
        'time': timezone.now().isoformat(),
        'endpoints': {
            'admin': f'{base}/admin/',
            'register': f'{base}/auth/register',
            'login': f'{base}/auth/login',
            'refresh_token': f'{base}/auth/refresh-token',
            'logout': f'{base}/auth/logout',
            'tasks': f'{base}/tasks/',
            'projects': f'{base}/annotations/projects/',
            'images': f'{base}/annotations/images/',
            'annotations': f'{base}/annotations/annotations/',
        },
    })
