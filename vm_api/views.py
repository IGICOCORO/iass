from rest_framework import viewsets
from .models import VirtualMachine
from .serializers import VirtualMachineSerializer

class VirtualMachineViewSet(viewsets.ModelViewSet):
    queryset = VirtualMachine.objects.all()
    serializer_class = VirtualMachineSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response