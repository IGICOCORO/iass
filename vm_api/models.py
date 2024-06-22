from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class VirtualMachine(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    is_enabled = models.BooleanField(default=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=48)

    def __str__(self):
        return self.name