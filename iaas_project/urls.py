from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('vm_api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]