from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import requests as axios

class ServeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serveur
        fields = '__all__'

    def to_representation(self, instance:Serveur):
        data = super().to_representation(instance)
        try:
            axios.get(f"http://{instance.ip}:8000/", timeout=1)
            data["online"] = True
        except Exception:
            data["online"] = False
        return data


class MicroVMSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroVM
        fields = '__all__'

    def to_representation(self, instance:MicroVM):
         data = super().to_representation(instance)
         data["serveur"] = ServeurSerializer(instance.serveur).data
         return data


class TokenPairSerializer(TokenObtainPairSerializer):

	def validate(self, attrs):
		data = super(TokenPairSerializer, self).validate(attrs)
		data['is_admin'] = self.user.is_superuser
		data['id'] = self.user.id
		return data