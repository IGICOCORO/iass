from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VirtualMachineViewSet

router = DefaultRouter()
router.register('vms', VirtualMachineViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
