from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('serveur', ServeurViewSet)
router.register('MicroVM', MicroVMViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
