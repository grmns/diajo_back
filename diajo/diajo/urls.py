from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ventas.urls')),  # URL de la aplicación de ventas
    path('compras/', include('compras.urls')),  # URL de la aplicación de compras
]
