import uuid
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Certificate
from .serializers import CertificateSerializer, PublicCertificateVerifySerializer
from accounts.permissions import IsTechspireAdmin

def get_certificate_by_code_or_id(code_or_id, select_related_extra=False):
    is_uuid = False
    try:
        uuid.UUID(str(code_or_id))
        is_uuid = True
    except (ValueError, AttributeError):
        is_uuid = False

    qs = Certificate.objects.all()
    if select_related_extra:
        qs = qs.select_related('course', 'course__category', 'user')
    else:
        qs = qs.select_related('course', 'user')

    if is_uuid:
        return qs.filter(Q(id=code_or_id) | Q(certificate_code__iexact=code_or_id)).first()
    return qs.filter(certificate_code__iexact=code_or_id).first()

class MyCertificatesListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CertificateSerializer
    pagination_class = None

    def get_queryset(self):
        return Certificate.objects.filter(user=self.request.user, is_valid=True).select_related('course', 'course__category', 'user')

class CertificateDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, code_or_id):
        cert = get_certificate_by_code_or_id(code_or_id, select_related_extra=True)

        if not cert:
            return Response({'error': 'Certificate not found.'}, status=status.HTTP_404_NOT_FOUND)

        if cert.user != request.user and not request.user.is_techspire_admin:
            return Response({'error': 'Unauthorized.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CertificateSerializer(cert)
        return Response(serializer.data)

class PublicVerifyCertificateView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, code_or_id):
        cert = get_certificate_by_code_or_id(code_or_id, select_related_extra=False)

        if not cert or not cert.is_valid:
            return Response({
                'is_valid': False,
                'error': 'Certificate not found or revoked.'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = PublicCertificateVerifySerializer(cert)
        return Response({
            'is_valid': True,
            'certificate': serializer.data
        }, status=status.HTTP_200_OK)

class AdminCertificateListView(generics.ListAPIView):
    permission_classes = (IsTechspireAdmin,)
    serializer_class = CertificateSerializer
    queryset = Certificate.objects.all().select_related('course', 'user').order_by('-issue_date')
