from django.db import models
from django.contrib.auth.models import User
# Create your models here.
    
class Serveur(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.GenericIPAddressField(max_length=48, unique=True)
    is_running = models.BooleanField(default=False, editable=False)

    def __str__(self) -> str:
        return f"{self.ip}"
    
class MicroVM(models.Model):
    id = models.AutoField(primary_key=True)
    serveur = models.ForeignKey(Serveur, on_delete=models.PROTECT)
    ip = models.GenericIPAddressField(max_length=48, editable=False)
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.ip}"