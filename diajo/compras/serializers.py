from rest_framework import serializers
from .models import Compra, Proveedor, Cuota

class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'
        
class CuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuota
        fields = '__all__'