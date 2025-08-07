from django.db import models
from .myuser import MyUser


class UserRelations(models.Model):
    refers_to = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='relations')
    _friends = models.ManyToManyField(MyUser, symmetrical=True, blank=True)
    _followers = models.ManyToManyField(MyUser, symmetrical=False, blank=True, related_name='+')
    _following = models.ManyToManyField(MyUser, symmetrical=False, blank=True, related_name='+')
    _silenced = models.ManyToManyField(MyUser, symmetrical=False, blank=True, related_name='+')
    _blocked = models.ManyToManyField(MyUser, symmetrical=False, blank=True, related_name='+')

    class Meta:
        verbose_name = "Relações de Usuário"
        verbose_name_plural = "Relações de Usuários"

    def __str__(self): return f"Relações de {getattr(self.refers_to.user, 'username', 'Usuário')}"

    @property
    def friends(self): return self._friends.all()
    @property
    def followers(self): return self._followers.all()
    @property
    def following(self): return self._following.all()
    @property
    def silenced(self): return self._silenced.all()
    @property
    def blocked(self): return self._blocked.all()

    def get_friends(self): return self.friends
    def get_friend(self, username): return self.__find_user_by_username(self.friends, username)
    def add_friend(self, user: MyUser):
        if user == self.refers_to:
            raise ValueError("Você não pode se adicionar como amigo.")
        if user in self.friends:
            raise ValueError("Usuário já é seu amigo.")
        self._friends.add(user)
        user.relations._friends.add(self.refers_to)
    def remove_friend(self, user: MyUser):
        if user == self.refers_to:
            raise ValueError("Você não pode se remover como amigo.")
        if user not in self.friends:
            raise ValueError("Usuário não é seu amigo.")
        self._friends.remove(user)
        user.relations._friends.remove(self.refers_to)

    def get_followers(self): return self.followers
    def get_follower(self, username): return self.__find_user_by_username(self.followers, username)
    def get_following(self): return self.following
    def get_following_user(self, username): return self.__find_user_by_username(self.following, username)
    def follow(self, user: MyUser):
        if user == self.refers_to:
            raise ValueError("Você não pode seguir a si mesmo.")
        if user in self.following:
            raise ValueError("Você já está seguindo este usuário.")
        self._following.add(user)
        user.relations._followers.add(self.refers_to)
    def unfollow(self, user: MyUser):
        if user == self.refers_to:
            raise ValueError("Você não pode deixar de seguir a si mesmo.")
        if user not in self.following:
            raise ValueError("Você não está seguindo este usuário.")
        self._following.remove(user)
        user.relations._followers.remove(self.refers_to)

    def get_silenced(self): return self.silenced
    def get_silenced_user(self, username): return self.__find_user_by_username(self.silenced, username)
    def silence(self, user: MyUser):
        if user == self.refers_to:
            raise ValueError("Você não pode silenciar a si mesmo.")
        if user in self.silenced:
            raise ValueError("Usuário já está silenciado.")
        self._silenced.add(user)
    def unsilence(self, user: MyUser):
        if user == self.refers_to:
            raise ValueError("Você não pode remover silêncio de si mesmo.")
        if user not in self.silenced:
            raise ValueError("Usuário não está silenciado.")
        self._silenced.remove(user)

    def get_blocked(self): return self.blocked
    def get_blocked_user(self, username): return self.__find_user_by_username(self.blocked, username)
    def block(self, user: MyUser):
        if user == self.refers_to:
            raise ValueError("Você não pode bloquear a si mesmo.")
        if user in self.blocked:
            raise ValueError("Usuário já está bloqueado.")
        self._blocked.add(user)
    def unblock(self, user: MyUser):
        if user == self.refers_to:
            raise ValueError("Você não pode desbloquear a si mesmo.")
        if user not in self.blocked:
            raise ValueError("Usuário não está bloqueado.")
        self._blocked.remove(user)

    def __find_user_by_username(self, user_list, username: str) -> MyUser | None:
        for user in user_list:
            if user.user.username == username: return user
        return None
