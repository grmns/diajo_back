from django.db import models
from datetime import timedelta, datetime, date
from django.utils.timezone import now
class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    ruc = models.CharField(max_length=11, unique=True)
    razon_social = models.CharField(max_length=255)

    def __str__(self):
        return self.razon_social

class Compra(models.Model):
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
        ('DFN', 'DE SCUENTO DE FACTURA NEGOCIABLE'),
        ('EFE', 'EFECTIVO'),
    ]

    id_compra = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    tipo_documento = models.IntegerField(choices=TIPO_DOCUMENTO_OPCIONES)
    DCTO_N = models.CharField(max_length=20)
    MONEDA = models.CharField(max_length=3, choices=OPCIONES_MONEDA, default=SOLES)
    IMPORTE = models.DecimalField(max_digits=10, decimal_places=2)
    PLAZO = models.IntegerField(null=True)
    FECHA_EMISION = models.DateField(null=True)
    RECEP_FT = models.DateField(null=True)
    FECHA_VENCIMIENTO = models.DateField(blank=True, null=True)
    CANCELADO = models.BooleanField(default=False)
    ANULADO = models.BooleanField(default=False)
    OBSERVACION = models.TextField(blank=True, null=True)
    FECHA_PAGO = models.DateField(blank=True, null=True)
    MODO_PAGO = models.CharField(max_length=10, choices=MODO_PAGO_OPCIONES, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.RECEP_FT and self.PLAZO:
            self.FECHA_VENCIMIENTO = self.RECEP_FT + timedelta(days=self.PLAZO)
        if self.CANCELADO and not self.FECHA_PAGO:
            self.FECHA_PAGO = datetime.now().date()
        super().save(*args, **kwargs)
        
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
        return f"Compra {self.DCTO_N} - Proveedor: {self.proveedor.razon_social}"
    

class Cuota(models.Model):
    numero_unico = models.CharField(max_length=20, unique=True, verbose_name="Número Único", blank=True, null=True)
    fecha_emision = models.DateField(default=now, verbose_name="Fecha de Emisión")
    plazo = models.IntegerField(verbose_name="Plazo en días", blank=True, null=True)
    fecha_vencimiento = models.DateField(verbose_name="Fecha de Vencimiento", null=True, blank=True)
    importe_cuota = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Importe de la Cuota")
    observacion = models.TextField(blank=True, null=True, verbose_name="Observación")
    fecha_pago = models.DateField(null=True, blank=True, verbose_name="Fecha de Pago")
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE, related_name="cuotas")

    def save(self, *args, **kwargs):
        if not self.id:  # Ejecuta solo si es una nueva instancia
            # Asegúrate de que compra_id se refiere a la clave primaria correcta de Compra
            compra = Compra.objects.get(id_compra=self.compra_id)
            self.fecha_vencimiento = self.fecha_emision + timedelta(days=self.plazo)
        super(Cuota, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.compra.DCTO_N} - {self.numero_unico}"