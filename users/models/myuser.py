from common.models import Timestamp
from django.contrib.auth.models import User
from django.db import models


class MyUser(Timestamp, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_permissions = models.OneToOneField("UserPermissions", on_delete=models.CASCADE, related_name='myuser')

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return getattr(self.user, 'username', 'Usuário')
