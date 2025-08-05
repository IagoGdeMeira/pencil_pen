from django.db import models
from datetime import datetime


class Timestamp(models.Model):
    _since_when = models.DateTimeField(auto_now_add=True)
    _updated_when = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
    @property
    def since_when(self) -> datetime: return self._since_when
    @property
    def updated_when(self) -> datetime: return self._updated_when

    def get_since_when(self) -> datetime: return self._since_when
    def get_updated_when(self) -> datetime: return self._updated_when

    def set_updated_when(self, d: datetime) -> None:
        self._updated_when = d
        self.save(update_fields=["_updated_when"])
