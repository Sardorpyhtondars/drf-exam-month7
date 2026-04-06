from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users.serializers import RegisterSerializer,LoginSerializer,LogoutSerializer,ProfileSerializer,PasswordResetRequestSerializer,PasswordResetConfirmSerializer


class RegisterAPIView(CreateAPIView):
    """POST /api/v1/users/register/ — Register a new user.
    - permission_classes = [AllowAny]
    - serializer_class = RegisterSerializer
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LoginAPIView(GenericAPIView):
    """POST /api/v1/users/login/ — Authenticate user and return JWT tokens.
    - permission_classes = [AllowAny]
    - serializer_class = LoginSerializer
    - post() must return access + refresh tokens
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutAPIView(GenericAPIView):
    """POST /api/v1/users/logout/ — Blacklist refresh token.
    - permission_classes = [IsAuthenticated]
    - serializer_class = LogoutSerializer
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)


class ProfileAPIView(RetrieveUpdateAPIView):
    """GET/PUT/PATCH /api/v1/users/profile/ — Retrieve or update current user profile.
    - permission_classes = [IsAuthenticated]
    - serializer_class = ProfileSerializer
    - get_object() returns request.user
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class PasswordResetRequestAPIView(GenericAPIView):
    """POST /api/v1/users/password-reset/ — Request a password reset email.
    - permission_classes = [AllowAny]
    - serializer_class = PasswordResetRequestSerializer
    """
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password reset email sent."}, status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(GenericAPIView):
    """POST /api/v1/users/password-reset/confirm/ — Confirm password reset.
    - permission_classes = [AllowAny]
    - serializer_class = PasswordResetConfirmSerializer
    """
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)