from django.db import models
from django.conf import settings
# Create your models here.
class UserProfile(models.Model):
    class Role(models.TextChoices):
        Manager = 'manager', 'Менеджер'
        User = 'user', 'Пользователь'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.User)

    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'{self.user.username} ({self.role})'

    @classmethod
    def for_user(cls, user):
        is_manager = user.is_superuser or user.is_staff
        profile, _created = cls.objects.get_or_create(
            user=user,
            defaults={
                'role': cls.Role.MANAGER if is_manager else cls.Role.User,
                'is_verified': is_manager
            },
        )
        return profile