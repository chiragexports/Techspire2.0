from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from .serializers import UserSerializer, RegisterSerializer, ProfileUpdateSerializer, AdminUserManageSerializer
from .permissions import IsTechspireAdmin

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Registration successful.'
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email_or_username = request.data.get('email') or request.data.get('username')
        password = request.data.get('password')

        if not email_or_username or not password:
            return Response({'error': 'Please provide email and password.'}, status=status.HTTP_400_BAD_REQUEST)

        # Allow login by email or username
        try:
            user = User.objects.get(Q(email__iexact=email_or_username) | Q(username__iexact=email_or_username))
            if not user.check_password(password):
                user = None
        except User.DoesNotExist:
            user = None

        if not user:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'error': 'User account is disabled.'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Login successful.'
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = ProfileUpdateSerializer(self.request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(self.request.user).data)

class AdminUserListView(generics.ListAPIView):
    permission_classes = (IsTechspireAdmin,)
    serializer_class = AdminUserManageSerializer

    def get_queryset(self):
        queryset = User.objects.all().order_by('-created_at')
        search = self.request.query_params.get('search', '').strip()
        role = self.request.query_params.get('role', '').strip()
        
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        if role:
            queryset = queryset.filter(role=role)
            
        return queryset

class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsTechspireAdmin,)
    queryset = User.objects.all()
    serializer_class = AdminUserManageSerializer
