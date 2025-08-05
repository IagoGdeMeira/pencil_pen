from django.db import models


class UserPermissions(models.Model):
    refers_to = models.OneToOneField("MyUser", on_delete=models.CASCADE, related_name='permissions')
    _friends_allowed = models.BooleanField(default=True)
    _followers_allowed = models.BooleanField(default=False)
    _followed_allowed = models.BooleanField(default=False)

    def __str__(self):
        return f"Permissões de {self.refers_to}"
    
    

    def are_friends_allowed(self) -> bool: return self._friends_allowed
    def are_followers_allowed(self) -> bool: return self._followers_allowed
    def are_followed_allowed(self) -> bool: return self._followed_allowed

    def set_friends_allowed(self, allowed: bool) -> None:
        self._friends_allowed = allowed
        self.save(update_fields=["_friends_allowed"])

    def set_followers_allowed(self, allowed: bool) -> None:
        self._followers_allowed = allowed
        self.save(update_fields=["_followers_allowed"])

    def set_followed_allowed(self, allowed: bool) -> None:
        self._followed_allowed = allowed
        self.save(update_fields=["_followed_allowed"])
