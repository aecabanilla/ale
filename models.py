from django.db import models
from django.utils import timezone

from .managers import DecidirManager, GireManager, SIRManager, ConciliacionManager


class DecidirCard(models.Model):
    id_operacion = models.CharField(max_length=255, help_text="Id de operacion", null=False)
    fecha_original = models.DateTimeField(null=False)
    monto = models.FloatField()
    cuotas = models.CharField(max_length=2, null=False)
    tarjeta = models.CharField(max_length=20, null=False)
    site = models.CharField(max_length=10, null=False)
    cod_aut = models.CharField(max_length=100, null=False)
    nro_tarjeta = models.CharField(max_length=100, null=False)
    titular = models.CharField(max_length=255, null=False)
    motivo = models.CharField(max_length=100, null=False)
    validacion_domicilio = models.CharField(max_length=100, null=False)
    validacion_titular = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    fecha_cierre = models.DateTimeField(null=False)
    estado_cierre = models.CharField(max_length=20, null=False)
    autent_externa = models.CharField(max_length=20, null=False)
    fecha_vto_cuota_1 = models.CharField(max_length=255, null=True)
    lote = models.CharField(max_length=255, null=True)
    usuario = models.CharField(max_length=50, null=True)
    confirmed = models.BooleanField(default=False)
    matched = models.BooleanField(default=False)
    timestamp = models.CharField(max_length=100)

    objects = DecidirManager()

    #Metadata
    #Métodos
    def __str__(self):
        return self.id_operacion

    class Meta:
        db_table = 'raw_data_decidir_card'

class DecidirPMC(models.Model):
    id_operacion = models.CharField(max_length=255, help_text="Id de operacion", null=False)
    fecha_original = models.DateTimeField(null=False)
    monto = models.FloatField()
    cuotas = models.CharField(max_length=2, null=False)
    tarjeta = models.CharField(max_length=20, null=False)
    site = models.CharField(max_length=10, null=False)
    cod_aut = models.CharField(max_length=100, null=False)
    nro_tarjeta = models.CharField(max_length=100, null=False)
    titular = models.CharField(max_length=255, null=False)
    motivo = models.CharField(max_length=100, null=False)
    validacion_domicilio = models.CharField(max_length=100, null=False)
    validacion_titular = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    fecha_ultima_modificacion = models.DateTimeField(null=False)
    estado = models.CharField(max_length=100)
    resultado_cs = models.CharField(max_length=100)
    estado_final = models.CharField(max_length=100)
    autent_vbv = models.CharField(max_length=100)
    tipo_doc = models.CharField(max_length=20)
    nro_doc = models.CharField(max_length=50)
    motivo_adicional = models.CharField(max_length=255)
    origen = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50, null=True)
    confirmed = models.BooleanField(default=False)
    matched = models.BooleanField(default=False)
    timestamp = models.CharField(max_length=100)

    objects = DecidirManager()

    class Meta:
        db_table = 'raw_data_decidir_pmc'


class GireModel(models.Model):

    raw_data = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255)
    fecha = models.CharField(max_length=50)
    importe = models.CharField(max_length=50)
    archivo = models.CharField(max_length=100)
    confirmed = models.BooleanField(default=False)
    matched = models.BooleanField(default=False)
    timestamp = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50, null=True)

    objects = GireManager()

    class Meta:
        db_table = 'raw_data_gire'


class OperationTypeModel(models.Model):
    id = models.CharField(max_length=50 ,primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'operation_types'


class SIRModel(models.Model):
    transaccion = models.CharField(max_length=255)
    medio_de_pago = models.CharField(max_length=100)
    monto = models.FloatField()
    fecha_de_pago = models.DateTimeField()
    estado_en_sir = models.BooleanField()
    dominio = models.TextField()
    cantidad_de_dominios = models.IntegerField()
    id_tad = models.IntegerField(max_length=255)
    codigo_de_tramite = models.ForeignKey(OperationTypeModel, on_delete=models.CASCADE)
    tipo_de_tramite = models.CharField(max_length=255)
    numero_de_factura = models.CharField(max_length=255)
    usuario = models.CharField(max_length=255)
    confirmed = models.BooleanField(default=False)
    matched = models.BooleanField(default=False)
    timestamp = models.CharField(max_length=100)

    objects = SIRManager()

    class Meta:
        db_table = 'raw_data_sir'


class ConciliacionModel(models.Model):

    transaccion = models.CharField(max_length=255)
    medio_de_pago = models.CharField(max_length=100)
    monto = models.FloatField()
    id_tad = models.IntegerField()
    fecha_de_pago = models.DateTimeField()
    dominios = models.CharField(max_length=255)
    numero_de_factura = models.CharField(max_length=255, default='', blank=True)
    estado_en_sir = models.BooleanField(default=False)
    codigo_de_tramite = models.ForeignKey(OperationTypeModel, on_delete=models.CASCADE)
    objects = ConciliacionManager()

    def __transaccion__(self):
        return self.transaccion

    class Meta:
        db_table = 'conciliacion'


class ResultModel(models.Model):

    month = models.IntegerField()
    year = models.IntegerField()
    amount = models.FloatField()
    payment_method = models.CharField(max_length=100)

    class Meta:
        db_table = 'results'


