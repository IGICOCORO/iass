from rest_framework import viewsets
from .models import VirtualMachine
from .serializers import VirtualMachineSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TokenPairSerializer
from rest_framework.permissions import IsAuthenticated


class VirtualMachineViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    queryset = VirtualMachine.objects.all()
    serializer_class = VirtualMachineSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response
    
class TokenPairView(TokenObtainPairView):
	serializer_class = TokenPairSerializer