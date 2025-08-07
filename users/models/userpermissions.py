from django.db import models


class UserPermissions(models.Model):
    _friends_allowed = models.BooleanField(default=True)
    _followers_allowed = models.BooleanField(default=False)
    _following_allowed = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Permissões de Usuário"
        verbose_name_plural = "Permissões de Usuários"

    def __str__(self): return "Permissões de Usuário"

    @property
    def friends_allowed(self) -> bool: return self._friends_allowed
    @property
    def followers_allowed(self) -> bool: return self._followers_allowed
    @property
    def following_allowed(self) -> bool: return self._following_allowed

    def are_friends_allowed(self) -> bool: return self._friends_allowed
    def set_friends_allowed(self, allowed: bool) -> None:
        self._friends_allowed = allowed
        self.save(update_fields=["_friends_allowed"])

    def are_followers_allowed(self) -> bool: return self._followers_allowed
    def set_followers_allowed(self, allowed: bool) -> None:
        self._followers_allowed = allowed
        self.save(update_fields=["_followers_allowed"])

    def are_following_allowed(self) -> bool: return self._following_allowed
    def set_following_allowed(self, allowed: bool) -> None:
        self._following_allowed = allowed
        self.save(update_fields=["_following_allowed"])
