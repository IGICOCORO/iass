from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('vm_api.urls')),
    path('', views.home, name='home'),
    path('<chemin>', views.home, name='home')
]