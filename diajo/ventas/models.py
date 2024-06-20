from django.db import models
from datetime import timedelta, date
from django.utils import timezone
from django.utils.timezone import now
from simple_history.models import HistoricalRecords
import json


# Modelo Vendedor modificado
class Vendedor(models.Model):
    ID_VENDEDOR = models.AutoField(primary_key=True)
    CODIGO = models.CharField(max_length=10, unique=True, null=True)  # Código del vendedor
    NOMBRE = models.CharField(max_length=100)  # Nombre del vendedor
    ACTIVO = models.BooleanField(default=True)  # Indica si el vendedor está activo
    RETIRADO = models.BooleanField(default=False)  # Indica si el vendedor está retirado

    def __str__(self):
        estado = "Retirado" if self.RETIRADO else "Activo"
        return f"{self.CODIGO} - {self.NOMBRE} ({estado})"
    
    
# Modelo Cliente modificado
class Cliente(models.Model):
    ID_CLIENTE = models.AutoField(primary_key=True)
    RUC = models.CharField(max_length=11, unique=True)
    RAZON_SOCIAL = models.CharField(max_length=100)
    razones_sociales_anteriores = models.TextField(blank=True, default='[]')  # Campo nuevo
    VENDEDOR = models.ForeignKey(Vendedor, on_delete=models.SET_NULL, null=True)
    TIPO_CLIENTE = models.IntegerField(choices=[(1, 'Cliente final'), (2, 'Subdistribuidor')], null=True)
    GRUPO_ECON = models.CharField(max_length=3, default='999')
    NOMBRE_GRUPO = models.CharField(max_length=100, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.RAZON_SOCIAL} ({self.RUC})"
    
    def save(self, *args, **kwargs):
        if self.pk:  # Verifica si el objeto ya está en la base de datos
            cliente_original = Cliente.objects.get(pk=self.pk)
            if cliente_original.RAZON_SOCIAL != self.RAZON_SOCIAL:
                razones_anteriores = json.loads(self.razones_sociales_anteriores)
                razones_anteriores.append(cliente_original.RAZON_SOCIAL)
                self.razones_sociales_anteriores = json.dumps(razones_anteriores, ensure_ascii=False)
        super().save(*args, **kwargs)

    def get_razones_sociales_anteriores_list(self):
        """Devuelve una lista ordenada de razones sociales anteriores."""
        return json.loads(self.razones_sociales_anteriores)
    
    
class HistorialRazonSocial(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='historial_razon_social', on_delete=models.CASCADE)
    razon_social_anterior = models.CharField(max_length=100)
    fecha_cambio = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-fecha_cambio']

    def __str__(self):
        return f"{self.razon_social_anterior} (Cambiado el {self.fecha_cambio})"

# Modelo Venta actualizado
class Venta(models.Model):
    # Constantes para las opciones de moneda
    SOLES = 'S/'
    DOLARES = 'USD'
    OPCIONES_MONEDA = [
        (SOLES, 'Soles'),
        (DOLARES, 'Dólares'),
    ]

    TIPO_DOCUMENTO_OPCIONES = [
        (1, 'Factura'),
        (2, 'Boleta'),
        (3, 'Nota de crédito'),
        (4, 'Nota de débito'),
        (5, 'Otro'),
    ]

    MODO_PAGO_OPCIONES = [
        ('CHE', 'CHEQUE'),
        ('LE', 'LETRA'),
        ('FCT', 'FACTORING'),
        ('TI', 'TRANSACCION INTERBANCARIA'),
        ('DFN', 'DESCUENTO DE FACTURA NEGOCIABLE'),
        ('EFE', 'EFECTIVO'),
    ]

    IT = models.AutoField(primary_key=True)  # Número correlativo automático

    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True)  # FK a Cliente
    tipo_documento = models.IntegerField(
        choices=TIPO_DOCUMENTO_OPCIONES, null=True)  # Tipo de documento
    DCTO_N = models.CharField(
        max_length=20)  # Número de documento
    MONEDA = models.CharField(
        max_length=3, choices=OPCIONES_MONEDA, default=SOLES)  # Moneda del importe
    # Monto en la moneda seleccionada
    IMPORTE = models.DecimalField(max_digits=10, decimal_places=2)
    PLAZO = models.IntegerField(null=True)  # Plazo de pago en días
    FECHA_EMISION = models.DateField(null=True)  # Fecha de emisión
    RECEP_FT = models.DateField(null=True)  # Fecha de recepción del documento
    FECHA_VENCIMIENTO = models.DateField(
        blank=True, null=True)  # Fecha de vencimiento
    # Si la venta ha sido cancelada
    CANCELADO = models.BooleanField(default=False)
    ANULADO = models.BooleanField(default=False)  # Si la venta ha sido anulada
    OBSERVACION = models.TextField(
        blank=True, null=True)  # Campo de observaciones
    # Fecha en que se realiza el pago
    FECHA_PAGO = models.DateField(blank=True, null=True)
    MODO_PAGO = models.CharField(
        max_length=10, choices=MODO_PAGO_OPCIONES, blank=True, null=True)  # Modo de pago
    COMISIONADO = models.BooleanField(
        default=False)  # Si la venta fue comisionada
    NUMERO_OPERACION = models.CharField(
        max_length=100, blank=True, null=True)  # Número de operación
    
    class Meta:
        unique_together = ('DCTO_N', 'tipo_documento',)  # Esto asegura la restricción

    def save(self, *args, **kwargs):
        # Calcular la fecha de vencimiento si no está establecida
        if not self.FECHA_VENCIMIENTO and self.RECEP_FT:
            self.FECHA_VENCIMIENTO = self.RECEP_FT + timedelta(days=self.PLAZO)

        # Establecer automáticamente la fecha de pago si la venta se marca como cancelada
        if self.CANCELADO and not self.FECHA_PAGO:
            self.FECHA_PAGO = now().date()

        super(Venta, self).save(*args, **kwargs)

    @property
    def ESTADO(self):
        if self.ANULADO:
            return 'Anulado'
        elif self.CANCELADO:
            return 'Cancelado'
        elif self.FECHA_VENCIMIENTO and date.today() > self.FECHA_VENCIMIENTO:
            return 'Vencido'
        else:
            return 'Vigente'

    def __str__(self):
        return f"{self.DCTO_N} - {self.cliente}"