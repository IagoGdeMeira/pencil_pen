from django.db import models


class UserRelations(models.Model):
    refers_to = models.OneToOneField("MyUser", on_delete=models.CASCADE, related_name='relations')
    _friends = models.ManyToManyField("self", symmetrical=True, blank=True)
    _followers = models.ManyToManyField("self", symmetrical=False, blank=True, related_name='followers')
    _following = models.ManyToManyField("self", symmetrical=False, blank=True, related_name='following')
    _silenced = models.ManyToManyField("self", symmetrical=False, blank=True, related_name='silenced')
    _blocked = models.ManyToManyField("self", symmetrical=False, blank=True, related_name='blocked')

    class Meta:
        verbose_name = "Relações de Usuário"
        verbose_name_plural = "Relações de Usuários"

    def __str__(self): return f"Relações de {getattr(self.refers_to, 'user.username', 'Usuário')}"

    @property
    def friends(self): return getattr(self._friends, 'all', lambda: [])()
    @property
    def followers(self): return getattr(self._followers, 'all', lambda: [])()
    @property
    def following(self): return getattr(self._following, 'all', lambda: [])()
    @property
    def silenced(self): return getattr(self._silenced, 'all', lambda: [])()
    @property
    def blocked(self): return getattr(self._blocked, 'all', lambda: [])()
    
    def get_friends(self): return self.friends
    def get_friend(self, username): return self.__find_user_by_username(self._friends, username)
    def add_friend(self, user: "MyUser"):
        if user == self.refers_to: raise ValueError("Você não pode se adicionar como amigo.")
        if user in self.friends: raise ValueError("Usuário já é seu amigo.")
        getattr(self._friends, 'add', lambda u: None)(user)
        getattr(user.friends, 'add', lambda u: None)(self)
        self.save(update_fields=["_friends"])
        user.save(update_fields=["_friends"])
    def remove_friend(self, user: "MyUser"):
        if user == self.refers_to: raise ValueError("Você não pode se remover como amigo.")
        if user not in self.friends: raise ValueError("Usuário não é seu amigo.")
        getattr(self._friends, 'remove', lambda u: None)(user)
        getattr(user.friends, 'remove', lambda u: None)(self)
        self.save(update_fields=["_friends"])
        user.save(update_fields=["_friends"])

    def get_followers(self): return self._followers
    def get_follower(self, username): return self.__find_user_by_username(self._followers, username)
    def get_following(self): return self._following
    def get_following_user(self, username): return self.__find_user_by_username(self._following, username)
    def follow(self, user: "MyUser"):
        if user == self.refers_to: raise ValueError("Você não pode seguir a si mesmo.")
        if user in self.following: raise ValueError("Você já está seguindo este usuário.")
        getattr(self._following, 'add', lambda u: None)(user)
        getattr(user.followers, 'add', lambda u: None)(self)
        self.save(update_fields=["_following"])
        user.save(update_fields=["_followers"])
    def unfollow(self, user: "MyUser"):
        if user == self.refers_to: raise ValueError("Você não pode deixar de seguir a si mesmo.")
        if user not in self.following: raise ValueError("Você não está seguindo este usuário.")
        getattr(self._following, 'remove', lambda u: None)(user)
        getattr(user.followers, 'remove', lambda u: None)(self)
        self.save(update_fields=["_following"])
        user.save(update_fields=["_followers"])

    def get_silenced(self): return self._silenced
    def get_silenced_user(self, username): return self.__find_user_by_username(self._silenced, username)
    def silence(self, user: "MyUser"):
        if user == self.refers_to: raise ValueError("Você não pode silenciar a si mesmo.")
        if user in self.silenced: raise ValueError("Usuário já está silenciado.")
        getattr(self._silenced, 'add', lambda u: None)(user)
        self.save(update_fields=["_silenced"])
    def unsilence(self, user: "MyUser"):
        if user == self.refers_to: raise ValueError("Você não pode remover silêncio de si mesmo.")
        if user not in self.silenced: raise ValueError("Usuário não está silenciado.")
        getattr(self._silenced, 'remove', lambda u: None)(user)
        self.save(update_fields=["_silenced"])

    def get_blocked(self): return self._blocked
    def get_blocked_user(self, username): return self.__find_user_by_username(self._blocked, username)
    def block(self, user: "MyUser"):
        if user == self.refers_to: raise ValueError("Você não pode bloquear a si mesmo.")
        if user in self.blocked: raise ValueError("Usuário já está bloqueado.")
        getattr(self._blocked, 'add', lambda u: None)(user)
        self.save(update_fields=["_blocked"])
    def unblock(self, user: "MyUser"):
        if user == self.refers_to: raise ValueError("Você não pode desbloquear a si mesmo.")
        if user not in self.blocked: raise ValueError("Usuário não está bloqueado.")
        getattr(self._blocked, 'remove', lambda u: None)(user)
        self.save(update_fields=["_blocked"])

    def __find_user_by_username(self, user_list, username):
        for relation in user_list:
            if relation.refers_to.user.username == username: return relation.refers_to
        return None
