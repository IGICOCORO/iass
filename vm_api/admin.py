from django.contrib import admin
from .models import *

@admin.register(Serveur)
class ServeurAdmin(admin.ModelAdmin):
    list_display = "id", "ip"

@admin.register(MicroVM)
class MicroVMModelAdmin(admin.ModelAdmin):
    list_display = "id", "nom", "serveur", "ip", "date_creation"
