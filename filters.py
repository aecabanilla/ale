import django_filters
from .models import DecidirCard, DecidirPMC, GireModel, SIRModel, ConciliacionModel, ResultModel
from datetime import datetime, timedelta


class DecidirCardFilter(django_filters.FilterSet):
    id_operacion = django_filters.CharFilter(lookup_expr='icontains')
    titular = django_filters.CharFilter(lookup_expr='icontains')
    fecha_desde = django_filters.DateFilter(method='fecha_desde_filter')
    fecha_hasta = django_filters.DateFilter(method='fecha_hasta_filter')
    estado_cierre = django_filters.CharFilter(method='estado_cierre_filter')
    motivo = django_filters.CharFilter(lookup_expr='icontains')
    tarjeta = django_filters.CharFilter(method='tarjeta_filter')
    monto_desde = django_filters.NumberFilter(method='monto_desde_filter')
    monto_hasta = django_filters.NumberFilter(method='monto_hasta_filter')
    lote = django_filters.NumberFilter()
    matched = django_filters.BooleanFilter(method='matched_filter')

    def matched_filter(self, queryset, name, value):
            if value == True:
                value = '1'
            elif value == False:
                value = '0'
            else:
                return queryset.filter(matched__isnull=False)  

            return queryset.filter(matched=value)

    def fecha_desde_filter(self, queryset, name, value):
        return queryset.filter(fecha_original__gte=value)

    def fecha_hasta_filter(self, queryset, name, value):
        return queryset.filter(fecha_original__lte=value + timedelta(days=1))

    def estado_cierre_filter(self, queryset, name, value):
        if (value):
            return queryset.filter(estado_cierre__in=value.split(','))

    def tarjeta_filter(self, queryset, name, value):
        if (value):
            return queryset.filter(tarjeta__in=value.split(','))

    def monto_desde_filter(self, queryset, name, value):
        return queryset.filter(monto__gte=value)

    def monto_hasta_filter(self, queryset, name, value):
        return queryset.filter(monto__lte=value)


    class Meta:
        model = DecidirCard
        fields = ['id_operacion', 'titular', 'fecha_desde', 'fecha_hasta', 'estado_cierre', 'motivo', 'tarjeta', 'monto_desde', 'monto_hasta', 'lote','matched']


class DecidirPMCFilter(django_filters.FilterSet):
    id_operacion = django_filters.CharFilter(lookup_expr='icontains')
    titular = django_filters.CharFilter(lookup_expr='icontains')
    fecha_desde = django_filters.DateFilter(method='fecha_desde_filter')
    fecha_hasta = django_filters.DateFilter(method='fecha_hasta_filter')
    estado = django_filters.CharFilter(method='estado_filter')
    motivo = django_filters.CharFilter(lookup_expr='icontains')
    tarjeta = django_filters.CharFilter(method='tarjeta_filter')
    monto_desde = django_filters.NumberFilter(method='monto_desde_filter')
    monto_hasta = django_filters.NumberFilter(method='monto_hasta_filter')
    matched = django_filters.BooleanFilter(method='matched_filter')

    def matched_filter(self, queryset, name, value):
            if value == True:
                value = '1'
            elif value == False:
                value = '0'
            else:
                return queryset.filter(matched__isnull=False)
                
            return queryset.filter(matched=value)

    def fecha_desde_filter(self, queryset, name, value):
        return queryset.filter(fecha_original__gte=value)

    def fecha_hasta_filter(self, queryset, name, value):
        return queryset.filter(fecha_original__lte=value)

    def estado_filter(self, queryset, name, value):
        if (value):
            return queryset.filter(estado__in=value.split(','))

    def tarjeta_filter(self, queryset, name, value):
        if (value):
            return queryset.filter(tarjeta__in=value.split(','))

    def monto_desde_filter(self, queryset, name, value):
        return queryset.filter(monto__gte=value)

    def monto_hasta_filter(self, queryset, name, value):
        return queryset.filter(monto__lte=value)


    class Meta:
        model = DecidirPMC
        fields = ['id_operacion', 'titular', 'fecha_desde', 'fecha_hasta', 'estado', 'motivo', 'tarjeta', 'monto_desde', 'monto_hasta','matched']



class GireFilter(django_filters.FilterSet):
    barcode = django_filters.CharFilter(lookup_expr='icontains')
    fecha = django_filters.CharFilter(lookup_expr='icontains')
    importe = django_filters.CharFilter(lookup_expr='icontains')
    archivo = django_filters.CharFilter(lookup_expr='icontains')
    matched = django_filters.BooleanFilter(method='matched_filter')

    def matched_filter(self, queryset, name, value):
            if value == True:
                value = '1'
            elif value == False:
                value = '0'
            else:
                return queryset.filter(matched__isnull=False)
                
            return queryset.filter(matched=value)


    class Meta:
        model = GireModel
        fields = ['barcode', 'fecha', 'importe', 'archivo']
        
        
class SIRFilter(django_filters.FilterSet):

    transaccion = django_filters.CharFilter(lookup_expr='icontains')
    medio_de_pago = django_filters.CharFilter(method='medio_de_pago_filter')
    monto_desde = django_filters.NumberFilter(method='monto_desde_filter')
    monto_hasta = django_filters.NumberFilter(method='monto_hasta_filter')
    fecha_de_pago_desde = django_filters.DateFilter(method='fecha_de_pago_desde_filter')
    fecha_de_pago_hasta = django_filters.DateFilter(method='fecha_de_pago_hasta_filter')
    dominio = django_filters.CharFilter(lookup_expr='icontains')
    tipo_de_tramite = django_filters.CharFilter(method='tipo_de_tramite_filter')
    matched = django_filters.BooleanFilter(method='matched_filter')
    estado_en_sir = django_filters.CharFilter(method='estado_en_sir_filter')

    def estado_en_sir_filter(self, queryset, name, value):
        if (value=='PAGO'):
            estado = True
        elif (value=='IMPAGO'):
            estado = False
        else:
            return queryset.filter(estado_en_sir__isnull = False)

        return queryset.filter(estado_en_sir=estado)

    def matched_filter(self, queryset, name, value):
            if value == True:
                value = '1'
            elif value == False:
                value = '0'
            else:
                return queryset.filter(matched_is_null = False)
                
            return queryset.filter(matched=value)

    def medio_de_pago_filter(self, queryset, name, value):
        if(value):
            return queryset.filter(medio_de_pago__in=value.split(','))

    def estado_filter(self, queryset, name, value):
        if(value):
            return queryset.filter(segundo_estado__in=value.split(','))

    def monto_desde_filter(self, queryset, name, value):
        return queryset.filter(monto__gte=value)

    def monto_hasta_filter(self, queryset, name, value):
        return queryset.filter(monto__lte=value)

    def fecha_de_pago_desde_filter(self, queryset, name, value):
        return queryset.filter(fecha_de_pago__gte=value)

    def fecha_de_pago_hasta_filter(self, queryset, name, value):
        return queryset.filter(fecha_de_pago__lte=value + timedelta(days=1))

    def tipo_de_tramite_filter(self, queryset, name, value):
        if (value):
            return queryset.filter(codigo_de_tramite__in=value.split(','))

    class Meta:
        model = SIRModel
        fields = ['transaccion', 'medio_de_pago', 'monto_desde', 'monto_hasta', 'fecha_de_pago_desde', 'fecha_de_pago_hasta', 'dominio', 'tipo_de_tramite','matched','estado_en_sir']


class ConciliacionFilter(django_filters.FilterSet):
    transaccion = django_filters.CharFilter(lookup_expr='icontains')
    medio_de_pago = django_filters.CharFilter(lookup_expr='icontains')
    monto_desde = django_filters.NumberFilter(method='monto_desde_filter')
    monto_hasta = django_filters.NumberFilter(method='monto_hasta_filter')
    id_tad = django_filters.NumberFilter()
    fecha_de_pago_desde = django_filters.DateFilter(method='fecha_de_pago_desde_filter')
    fecha_de_pago_hasta = django_filters.DateFilter(method='fecha_de_pago_hasta_filter')
    dominios = django_filters.CharFilter(lookup_expr='icontains')
    codigo_de_tramite = django_filters.CharFilter(method='codigo_de_tramite_filter')
    numero_de_factura = django_filters.CharFilter(method='numero_de_factura_filter')
    estado_en_sir = django_filters.CharFilter(method='estado_en_sir_filter')

    def estado_en_sir_filter(self, queryset, name, value):
        if (value=='PAGO'):
            estado = True
        elif (value=='IMPAGO'):
            estado = False
        else:
            return queryset.filter(estado_en_sir__isnull = False)

        return queryset.filter(estado_en_sir=estado)

    def numero_de_factura_filter(self, queryset, name, value):
            return queryset.filter(numero_de_factura=value)

    def monto_desde_filter(self, queryset, name, value):
        return queryset.filter(monto__gte=value)

    def monto_hasta_filter(self, queryset, name, value):
        return queryset.filter(monto__lte=value)

    def fecha_de_pago_desde_filter(self, queryset, name, value):
        return queryset.filter(fecha_de_pago__gte=value)

    def fecha_de_pago_hasta_filter(self, queryset, name, value):
        return queryset.filter(fecha_de_pago__lte=value + timedelta(days=1))

    def codigo_de_tramite_filter(self, queryset, name, value):
        if (value):
            return queryset.filter(codigo_de_tramite__in=value.split(','))

    class Meta:
        model = ConciliacionModel
        fields = ['transaccion', 'medio_de_pago', 'monto_desde', 'monto_hasta', 'id_tad', 'fecha_de_pago_desde',
                  'fecha_de_pago_hasta', 'dominios', 'codigo_de_tramite']


class ResultFilter(django_filters.FilterSet):
    month = django_filters.NumberFilter()
    year = django_filters.NumberFilter()
    amount = django_filters.NumberFilter()
    payment_method = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ResultModel
        fields = ['month', 'year', 'amount', 'payment_method']
