import json
from rest_framework import viewsets
from .models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import *
import requests as axios

def hexa(x):
     value = hex(x)[2:].upper()
     if len(value) == 1:
          return f"0{value}"
     return value

class ServeurViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    queryset = Serveur.objects.all()
    serializer_class = ServeurSerializer
    permission_classes = [IsAuthenticated]

class MicroVMViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    queryset = MicroVM.objects.all()
    serializer_class = MicroVMSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = MicroVMSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        serveur:Serveur = data["serveur"]

        mvms = MicroVM.objects.all()
        if not mvms.exists():
             magic_numbers = [0, 1]
        else:
             last = MicroVM.objects.last()
             ip = last.ip.split(".")
             magic_numbers = [int(ip[-2]), int(ip[-1])+3]

        if magic_numbers[1] > 252:
             magic_numbers[0] += 1
             magic_numbers[1] = magic_numbers[1] % 255
             
        tap_numbers = [172, 10, magic_numbers[0], magic_numbers[1]]
        eth_numbers = [172, 10, magic_numbers[0], magic_numbers[1] + 1]
        mac_numbers = [6, 0, 172, 10, magic_numbers[0], magic_numbers[1] + 1]

        dictionaire = {
            "id": 255 * magic_numbers[0] + magic_numbers[1],
            "name": data["nom"],
            "eth_ip": ".".join([str(x) for x in eth_numbers]),
            "tap_ip": ".".join([str(x) for x in tap_numbers]),
            "fc_mac": ":".join([hexa(x) for x in mac_numbers])
        }
        response = axios.post(f"http://{serveur.ip}:8000/micro_vms/", dictionaire)
        serializer.save(ip = dictionaire["eth_ip"])
        for server in Serveur.objects.all():
             data = {
                  "server_ip": serveur.ip,
                  "micro_vm_ip": dictionaire["eth_ip"],
             }
             axios.post(f"http://{server.ip}:8000/ip_tables/", data)
        return Response(json.loads(response.text), 201)
    
    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated], url_name=r'resend', url_path=r"resend")
    def resend(self, request, pk):
        micro_vm:MicroVM = self.get_object()
        reponse = []
        for server in Serveur.objects.all():
            data = {
                "server_ip": micro_vm.serveur.ip,
                "micro_vm_ip": micro_vm.ip,
            }
            result = {"server": str(micro_vm.serveur)}
            try:
                axios_reponse = axios.post(f"http://{server.ip}:8000/ip_tables/", data, timeout=3)
                result["response"] = axios_reponse.json()
            except Exception as e:
                result["response"] = str(e)
            reponse.append(result)
            
        return Response(reponse, 200)
    
    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated], url_name=r'restart', url_path=r"restart")
    def restart(self, request, pk):
        micro_vm:MicroVM = self.get_object()
        reponse = []
        try:
            axios.get(f"http://{micro_vm.serveur.ip}:8000/micro_vms/{micro_vm.id}/restart/")
        except Exception as e:
             return Response({"status": str(e)}, 400)
        for server in Serveur.objects.all():
            data = {
                "server_ip": micro_vm.serveur.ip,
                "micro_vm_ip": micro_vm.ip,
            }
            result = {"server": str(micro_vm.serveur)}
            try:
                axios_reponse = axios.post(f"http://{server.ip}:8000/ip_tables/", data, timeout=3)
                result["response"] = axios_reponse.json()
            except Exception as e:
                result["response"] = str(e)
            reponse.append(result)
            
        return Response(reponse, 200)
        
    
class TokenPairView(TokenObtainPairView):
	serializer_class = TokenPairSerializer