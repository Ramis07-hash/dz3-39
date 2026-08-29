from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

# drf-spectacular импорттору
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes,
)

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


@extend_schema(
    tags=['users'],
    summary="Колдонуучуну каттоо",
    description="Жаңы колдонуучуну каттоодон өткөрөт жана түзүлгөн профилдин маалыматтарын кайтарат.",
    request=RegisterSerializer,
    responses={
        201: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    }
)
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


@extend_schema(
    tags=['users'],
    summary="Token авторизациясы (Логин)",
    description="Колдонуучунун логин жана паролу аркылуу DRF Token алуу.",
    request=LoginSerializer,
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    }
)
class TokenLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user, error = _check_password(request)
        if error:
            return error
        return Response(token_payload(user))


@extend_schema(
    tags=['users'],
    summary="Token аркылуу системадан чыгуу (Системадан чыгуу)",
    description="Авторизацияланган колдонуучунун DRF Tokenин өчүрөт.",
    responses={
        204: None,
        401: OpenApiTypes.OBJECT,
    }
)
class TokenLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=['users'],
    summary="JWT авторизациясы (Логин)",
    description="Колдонуучунун логин жана паролу аркылуу JWT (Access жана Refresh) токендерин алуу.",
    request=LoginSerializer,
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    }
)
class JWTLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user, error = _check_password(request)
        if error:
            return error
        return Response(jwt_payload(user))


@extend_schema(
    tags=['users'],
    summary="JWT Токенди жаңылоо (Refresh Token)",
    description="Refresh токен аркылуу жаңы Access токен алуу."
)
class JWTRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)


@extend_schema(
    tags=['users'],
    summary="Учурдагы колдонуучунун профилин алуу (Me)",
    description="Авторизациядан өткөн колдонуучунун жеке маалыматтарын кайтарат.",
    responses={
        200: OpenApiTypes.OBJECT,
        401: OpenApiTypes.OBJECT,
    }
)
class MeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(profile_data(request.user))


@extend_schema_view(
    get=extend_schema(
        tags=['users'],
        summary="Бардык колдонуучулардын тизмесин алуу",
        description="Системадагы бардык колдонуучулардын профилдерин алуу (Менеджерлер үчүн гана).",
        responses={
            200: UserProfileSerializer(many=True),
            403: OpenApiTypes.OBJECT,
        }
    )
)
class UserListView(generics.ListAPIView):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsManager,)


@extend_schema(
    tags=['users'],
    summary="Колдонуучуну верификациялоо (Тастыктоо)",
    description="Колдонуучунун профилин `is_verified=True` катары белгилөө (Менеджерлер үчүн гана).",
    parameters=[
        OpenApiParameter(
            name='pk',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="Верификация кылынуучу UserProfile ID номери"
        )
    ],
    request=None,
    responses={
        200: UserProfileSerializer,
        403: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
    }
)
class VerifyUserView(APIView):
    permission_classes = (IsManager,)

    def post(self, request, pk):
        profile = get_object_or_404(UserProfile, pk=pk)
        profile.is_verified = True
        profile.save(update_fields=['is_verified'])
        return Response(UserProfileSerializer(profile).data)