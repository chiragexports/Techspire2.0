from django.urls import path
from .views import MyCertificatesListView, CertificateDetailView, PublicVerifyCertificateView, AdminCertificateListView

urlpatterns = [
    path('certificates/my-certificates/', MyCertificatesListView.as_view(), name='my_certificates'),
    path('certificates/<str:code_or_id>/', CertificateDetailView.as_view(), name='certificate_detail'),
    path('certificates/verify/<str:code_or_id>/', PublicVerifyCertificateView.as_view(), name='verify_certificate'),
    path('admin/certificates/', AdminCertificateListView.as_view(), name='admin_certificates'),
]
