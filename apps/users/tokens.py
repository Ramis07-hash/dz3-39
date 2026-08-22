"""
Два способа сказать API: «это я».

1) Token  -  Authorization: Token <ключ>
   Ключ лежит в таблице authtoken_token. Пока строка есть - вход действует
   Выход = удалить строку из базы

2) JWT  -  Authorization: Bearer <access>
   В базе токен НЕ хранится. Сервер только проверяет подпись (SECRET_KEY)
   access живёт недолго, refresh нужен - чтобы получить новый access
   Выйти из аккаунты значит удалить access и refresh на клиенте
   Или же они истекают по сроку действия
"""

from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile
from .serializers import UserProfileSerializer


def profile_data(user):
    profile = UserProfile.for_user(user)
    return UserProfileSerializer(profile).data


def token_payload(user):
    """Вариант 1. Один ключ, он же в БД."""
    token, _created = Token.objects.get_or_create(user=user)
    return {
        'auth_type': 'token',
        'token': token.key,
        'profile': profile_data(user),
    }


def jwt_payload(user):
    """Вариант 2. Пара ключей, в БД их нет — только подпись."""
    refresh = RefreshToken.for_user(user)
    return {
        'auth_type': 'jwt',
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'profile': profile_data(user),
    }
