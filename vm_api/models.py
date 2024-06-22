from django.db import models

# Create your models here.

class VirtualMachine(models.Model):
    name = models.CharField(max_length=100)
    is_enabled = models.BooleanField(default=False)
    cpu = models.IntegerField()
    memory = models.IntegerField()

    def __str__(self):
        return self.name