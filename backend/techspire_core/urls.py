import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'status': 'online',
        'platform': 'Techspire Technical Education Platform',
        'version': '2.0.0',
        'documentation': '/api/docs/'
    })

# Unified API endpoints
api_patterns = [
    path('', api_root, name='api_root'),
    path('auth/', include('accounts.urls')),
    path('auth', include('accounts.urls')),
    path('', include('courses.urls')),
    path('', include('progress.urls')),
    path('', include('assessments.urls')),
    path('', include('certificates.urls')),
    path('', include('analytics.urls')),
    path('payments/', include('payments.urls')),
    path('payments', include('payments.urls')),
]

urlpatterns = [
    path('api/backend/', include(api_patterns)),
    path('api/backend', include(api_patterns)),
    path('api/', include(api_patterns)),
    path('api', include(api_patterns)),
    path('backend/', include(api_patterns)),
    path('backend', include(api_patterns)),
    path('', include(api_patterns)),
]

# Admin enabled in DEBUG or when explicitly configured
if settings.DEBUG or os.getenv('ENABLE_DJANGO_ADMIN', 'False') == 'True':
    urlpatterns.append(path('admin/', admin.site.urls))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
