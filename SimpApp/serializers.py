from rest_framework import serializers
from SimpApp.models import MyUser
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from SimpApp.utils import Util


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=58, min_length=10, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                "Username should only contain alphanumeric characters")
        return attrs

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = MyUser
        fields = ["token"]


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=10)
    password = serializers.CharField(
        max_length=72, min_length=10, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=10, read_only=True)
    tokens = serializers.CharField(
        max_length=68, min_length=6, read_only=True)

    class Meta:

        model = MyUser
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, Try again")

        if not user.is_active:
            raise AuthenticationFailed("Account disabled")

        if not user.is_verified:
            raise AuthenticationFailed("Account is not verified")

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super.validate(attrs)


class ResetPasswordEmailRequestSerializer(serializers.Serializer):

    email = serializers.EmailField(min_length=6)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=70, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:

        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):

        try:
            password = attrs.get('password', '')
            token = attrs.get('token', '')
            uidb64 = attrs.get('uidb64', '')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = MyUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return AuthenticationFailed("The reset link is invalid", 400)

            user.set_password(password)
            user.save()

            return user

        except Exception as e:
            return AuthenticationFailed("The reset link is invalid", 400)

        return super().validate(attrs)
