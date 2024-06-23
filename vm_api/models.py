from django.db import models
from django.contrib.auth.models import User
# Create your models here.
    
class Serveur(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=48)
    RAM = models.PositiveIntegerField()
    disk = models.PositiveBigIntegerField()
    ip_address = models.CharField(max_length=48)
    nbres_vm = models.PositiveBigIntegerField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.name}"
    
class MicroVM(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=48)
    is_enabled = models.BooleanField(default=False)
    serveur = models.ForeignKey(Serveur, on_delete=models.PROTECT)
    os = models.CharField(max_length=48)
    ip_address = models.CharField(max_length=48)
    taille = models.PositiveBigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name}"