from django.contrib import admin

# Register your models here.
from .models import Proveedor, Compra, Cuota

admin.site.register(Proveedor)

admin.site.register(Compra)

admin.site.register(Cuota)