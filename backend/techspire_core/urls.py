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

urlpatterns = [
    path('', api_root, name='root'),
    path('api/', api_root, name='api_root'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('progress.urls')),
    path('api/', include('assessments.urls')),
    path('api/', include('certificates.urls')),
    path('api/', include('analytics.urls')),
    path('api/payments/', include('payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
