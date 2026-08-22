from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from .models import UserProfile
from .permissions import IsManager
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserProfileSerializer,
)
from .tokens import jwt_payload, profile_data, token_payload


def _check_password(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(
        username=serializer.validated_data['username'],
        password=serializer.validated_data['password'],
    )
    if user is None:
        return None, Response(
            {'detail': 'Неверный логин или пароль.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return user, None


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {'profile': profile_data(user)},
            status=status.HTTP_201_CREATED,
        )


class TokenLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user, error = _check_password(request)
        if error:
            return error
        return Response(token_payload(user))


class TokenLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JWTLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user, error = _check_password(request)
        if error:
            return error
        return Response(jwt_payload(user))


class JWTRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)


class MeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(profile_data(request.user))


class UserListView(generics.ListAPIView):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsManager,)


class VerifyUserView(APIView):
    permission_classes = (IsManager,)

    def post(self, request, pk):
        profile = get_object_or_404(UserProfile, pk=pk)
        profile.is_verified = True
        profile.save(update_fields=['is_verified'])
        return Response(UserProfileSerializer(profile).data)
