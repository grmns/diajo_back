# ventas/forms.py

from django import forms
from .models import Venta, Cliente

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['vendedor', 'cliente', 'tipo_documento', 'DCTO_N', 'MONEDA', 'IMPORTE', 
                  'PLAZO', 'FECHA_EMISION', 'RECEP_FT', 'CANCELADO']

    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.all()
        self.fields['cliente'].label_from_instance = lambda obj: f"{obj.RAZON_SOCIAL} ({obj.RUC})"

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['RUC', 'RAZON_SOCIAL', 'DIRECCION_LEGAL', 'CODIGO', 
                  'TIPO_CLIENTE', 'GRUPO_ECON', 'NOMBRE_GRUPO']
