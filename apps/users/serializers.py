from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    """
    Validates registration input.
    Fields: username, email, password, confirm_password.
    - Validate that password == confirm_password
    - Validate email is unique
    - create() must hash the password and create the user
    """
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

class LoginSerializer(serializers.Serializer):
    """
    Validates login credentials.
    Fields: email, password.
    - Must authenticate user with email+password
    - Return error if credentials are invalid
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account is disabled.")
        data['user'] = user
        return data

class LogoutSerializer(serializers.Serializer):
    """
    Accepts a refresh token for blacklisting.
    Fields: refresh
    - save() must blacklist the given refresh token
    """
    refresh = serializers.CharField()
    def save(self):
        token = RefreshToken(self.validated_data['refresh'])
        token.blacklist()

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializes user profile for read and update.
    Model: CustomUser
    Fields: id, username, email, first_name, last_name, bio, avatar, website, date_joined
    Read-only: id, email, date_joined
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'bio', 'avatar', 'website', 'date_joined']
        read_only_fields = ['id', 'email', 'date_joined']

class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Validates password reset request.
    Fields: email
    - Must verify email exists in the system
    """
    email = serializers.EmailField()
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No account found with this email.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Validates password reset confirmation.
    Fields: token, new_password, confirm_password
    - Validate token is valid
    - Validate new_password == confirm_password
    """
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def save(self):
        from django.utils.http import urlsafe_base64_decode
        token = self.validated_data['token']
        try:
            uid = urlsafe_base64_decode(token).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError):
            raise serializers.ValidationError("Invalid or expired token.")
        user.set_password(self.validated_data['new_password'])
        user.save()

        # I couldn't do it myself