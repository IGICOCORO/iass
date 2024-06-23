from rest_framework import viewsets
from .models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class ServeurViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    queryset = Serveur.objects.all()
    serializer_class = ServeurSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = SessionAuthentication,

class MicroVMViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    queryset = MicroVM.objects.all()
    serializer_class = MicroVMSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = SessionAuthentication,
    
    def create(self, request, *args, **kwargs):
        serializer = MicroVMSerializer(data=request.data)
        serializer.validated_data(raise_exception=True)
        data = serializer.validated_data

        mvms = MicroVM.objects.all()
        if mvms.exists():
             magic_numbers = [0, 1]
        else:
             last = MicroVM.objects.last()
             ip = last.ip_address.split(".")
             magic_numbers = [int(ip[-1]), int(ip[-2])+4]

        if magic_numbers[1] > 252:
             magic_numbers[1] = 1
             magic_numbers[0] += 1
             
        tap_numbers = [172, 16, magic_numbers[0], magic_numbers[1]]
        eth_numbers = [172, 16, magic_numbers[0], magic_numbers[1] + 1]
        mac_numbers = [6, 0, 172, 10, magic_numbers[0], magic_numbers[1] + 1]

        dictionaire = {
            "name": data["name"],
            "eth_ip": ".".join(eth_numbers),
            "tap_ip": ".".join(tap_numbers),
            "fc_mac": ".".join([hex(x)[2:].upper() for x in mac_numbers])
        }
        return Response(dictionaire, 201)
    
class TokenPairView(TokenObtainPairView):
	serializer_class = TokenPairSerializer