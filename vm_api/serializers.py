from rest_framework import serializers
from .models import VirtualMachine
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class VirtualMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualMachine
        fields = '__all__'


class TokenPairSerializer(TokenObtainPairSerializer):

	def validate(self, attrs):
		data = super(TokenPairSerializer, self).validate(attrs)
		data['is_admin'] = self.user.is_superuser
		data['id'] = self.user.id
		return data