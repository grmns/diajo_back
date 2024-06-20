from django.contrib import admin

# Register your models here.
from .models import Venta, Cliente, Vendedor, HistorialRazonSocial

admin.site.register(Venta)
admin.site.register(Cliente)
admin.site.site_header = "Sistema de Ventas"
admin.site.register(Vendedor)
admin.site.register(HistorialRazonSocial)