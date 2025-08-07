from common.models import Timestamp
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class MyUser(Timestamp, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    relations = models.OneToOneField("UserRelations", on_delete=models.CASCADE, related_name='user_relations')
    profile_permissions = models.ForeignKey("UserPermissions", on_delete=models.CASCADE, related_name='users_with_permissions')
    
    _nickname = models.CharField(max_length=100, blank=True, null=True)  # Alterado de _shown_name para _nickname
    _biography = models.TextField(max_length=300, blank=True, null=True)
    _profile_pic_path = models.CharField(max_length=255, blank=True, null=True)
    _set_to_deletion_when = models.DateTimeField(blank=True, null=True)
    _accessable = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self): return getattr(self.user, 'username', 'Usuário')
    
    @property
    def nickname(self) -> str:
        return self._nickname or getattr(self.user, 'username', 'Usuário')

    def get_nickname(self) -> str:
        return self._nickname

    def set_nickname(self, nickname: str) -> None:
        if not nickname:
            raise ValueError("O apelido não pode ser vazio.")
        if len(nickname) < 4:
            raise ValueError("O apelido não pode ter menos de 4 caracteres.")
        if len(nickname) > self._nickname.max_length:
            raise ValueError("O apelido não pode ter mais de 100 caracteres.")
        self._nickname = nickname
        self.save(update_fields=["_nickname"])

    def get_biography(self) -> str: return self._biography
    def set_biography(self, biography: str) -> None:
        if not biography: raise ValueError("A biografia não pode ser vazia.")
        if len(biography) > self._biography.max_length: raise ValueError("A biografia não pode ter mais de 300 caracteres.")
        self._biography = biography
        self.save(update_fields=["_biography"])

    def get_profile_pic_path(self) -> str: return self._profile_pic_path
    def set_profile_pic_path(self, path: str) -> None:
        if not path: raise ValueError("O caminho da foto de perfil não pode ser vazio.")
        if len(path) > self._profile_pic_path.max_length: raise ValueError("O caminho da foto de perfil não pode ter mais de 255 caracteres.")
        self._profile_pic_path = path
        self.save(update_fields=["_profile_pic_path"])

    def get_set_to_deletion_when(self) -> datetime: return self._set_to_deletion_when
    def set_set_to_deletion_when(self, d: datetime) -> None:
        if not isinstance(d, datetime): raise ValueError("A data de exclusão deve ser um objeto datetime.")
        if d < datetime.now(): raise ValueError("A data de exclusão não pode ser no passado.")
        self._set_to_deletion_when = d
        self.save(update_fields=["_set_to_deletion_when"])

    def get_accessable(self) -> bool: return self._accessable
    def set_accessable(self, accessable: bool) -> None:
        self._accessable = accessable
        self.save(update_fields=["_accessable"])
