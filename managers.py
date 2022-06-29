import datetime

from django.db import models, IntegrityError, connection

import pandas as pd
import logging

logger = logging.getLogger(__name__)

logger.setLevel(logging.WARNING)
handler = logging.FileHandler('/var/www/conciliacion/logs/logger_file.log')
formatter = logging.Formatter('%(asctime)s : %(name)s  : %(funcName)s : %(levelname)s : %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
from django.db.models import CharField, Value
from django.core.management import call_command

class ConciliacionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class DecidirManager(models.Manager):

    def insert_decidir_excel_card_values(self, request):

        timestamp = datetime.datetime.now().timestamp()

        results = {
            'i': 0,
            'duplicate': 0,
            'timestamp': timestamp
        }

        file = request.FILES['decidir_file']

        df = pd.read_excel(file.read(), engine='openpyxl')
        df = df.iloc[3:]

        for index, row in df.iterrows():

            try:


                self.create(
                    id_operacion=row.values[0].strip(),
                    fecha_cierre=row.values[1],
                    fecha_original=row.values[2],
                    monto=row.values[3].replace('$', '').strip(),
                    cuotas=row.values[4],
                    estado_cierre=row.values[5],
                    autent_externa=row.values[6] if str(row.values[6]) != 'nan' else 'N/A',
                    tarjeta=row.values[7],
                    site=row.values[8],
                    cod_aut=row.values[9],
                    nro_tarjeta=row.values[10],
                    titular=row.values[11],
                    motivo=row.values[12] if str(row.values[12]) != 'nan' else '',
                    validacion_domicilio=row.values[13],
                    validacion_titular=row.values[14] if str(row.values[14]) != 'nan' else None,
                    email=row.values[15] if str(row.values[15]) != 'nan' else None,
                    fecha_vto_cuota_1=row.values[16] if str(row.values[16]) != 'nan' else None,
                    lote=request.POST['lote'] if request.POST['lote'] else None,
                    usuario=request.user.username,
                    timestamp=timestamp
                )


                results['i'] += 1
            except IntegrityError as e:
                results['duplicate'] += 1
            except Exception as e:
                a = e

        return results


    def confirm_upload_card(self, timestamp):

        with connection.cursor() as cursor:
            cursor.execute("UPDATE raw_data_decidir_card SET confirmed=true WHERE confirmed=false and timestamp='%s'" % timestamp)

        call_command('process_decidir_card_payments')

    def cancel_upload_card(self, timestamp):

        with connection.cursor() as cursor:
            cursor.execute("delete from raw_data_decidir_card where timestamp='%s' and confirmed=false" % timestamp)


    def insert_decidir_excel_pmc_values(self, request):

        timestamp = datetime.datetime.now().timestamp()

        results = {
            'i': 0,
            'duplicate': 0,
            'timestamp': timestamp
        }

        file = request.FILES['decidir_file']

        df = pd.read_excel(file.read(), engine='openpyxl')


        for index, row in df.iterrows():

            try:

                self.create(
                    id_operacion=row.values[0].strip(),
                    fecha_ultima_modificacion=row.values[1],
                    fecha_original=row.values[2],
                    monto=row.values[3],
                    cuotas=row.values[4],
                    estado=row.values[5],
                    resultado_cs=row.values[6] if str(row.values[6]) != 'nan' else None,
                    estado_final=row.values[7],
                    autent_vbv=row.values[8] if str(row.values[8]) != 'nan' else None,
                    tarjeta=row.values[9],
                    site=row.values[10],
                    cod_aut=row.values[11],
                    nro_tarjeta=row.values[12],
                    titular=row.values[13],
                    tipo_doc=row.values[14],
                    nro_doc=row.values[15],
                    motivo=row.values[16] if str(row.values[16]) != 'nan' else None,
                    motivo_adicional=row.values[17] if str(row.values[17]) != 'nan' else None,
                    origen=row.values[18],
                    validacion_domicilio=row.values[19],
                    validacion_titular=row.values[20] if str(row.values[20]) != 'nan' else None,
                    email=row.values[21] if str(row.values[21]) != 'nan' else None,
                    usuario=request.user.username,
                    timestamp=timestamp
                )

                results['i'] += 1
            except IntegrityError as e:
                results['duplicate'] += 1
            except Exception as e:
                a = e

        return results

    def confirm_upload_pmc(self, timestamp):

        with connection.cursor() as cursor:
            cursor.execute("UPDATE raw_data_decidir_pmc SET confirmed=true WHERE confirmed=false and timestamp='%s'" % timestamp)

        call_command('process_decidir_pmc_payments')

    def cancel_upload_pmc(self, timestamp):

        with connection.cursor() as cursor:
            cursor.execute(
                "delete from raw_data_decidir_pmc where timestamp='%s' and confirmed=false" % timestamp)


class GireManager(models.Manager):

    def insert_values(self, request):

        timestamp = datetime.datetime.now().timestamp()

        results = {
            'i': 0,
            'duplicate': 0,
            'timestamp': timestamp
        }

        file = request.FILES['gire_file']

        for line in file:
            data = line.decode('unicode_escape')

            if len(data) == 76:

                try:
                    self.create(
                        raw_data=data,
                        fecha=data[1:9],
                        barcode=data[9:61].strip(),
                        importe=data[61:],
                        archivo=file.name,
                        usuario=request.user.username,
                        timestamp=timestamp
                    )

                    results['i'] += 1
                except IntegrityError as e:
                    results['duplicate'] += 1

        return results


    def confirm_upload(self, timestamp):

        with connection.cursor() as cursor:
            cursor.execute("UPDATE raw_data_gire SET confirmed=true WHERE confirmed=false and timestamp='%s'" % timestamp)

        call_command('process_gire_payments')

    def cancel_upload(self, timestamp):
        with connection.cursor() as cursor:
            cursor.execute(
                "delete from raw_data_gire where timestamp='%s' and confirmed=false" % timestamp)


class SIRManager(models.Manager):

    def get_nro_factura(pk):
        kk = models.objects.get(transaccion=pk).nro_de_factura
        return kk

    def insert_values(self, request):

        from .models import OperationTypeModel, SIRModel

        timestamp = datetime.datetime.now().timestamp()

        results = {
            'i': 0,
            'duplicate': 0,
            'timestamp': timestamp
        }

        file = request.FILES['sir_file']

        df = pd.read_excel(file.read(), engine='openpyxl')

        for index, row in df.iterrows():

            try:
                obj_sir = self.create(
                    transaccion=row.values[0],
                    medio_de_pago=row.values[1],
                    monto=row.values[2],
                    dominio=row.values[5],
                    cantidad_de_dominios=row.values[6],
                    id_tad=row.values[7],
                    tipo_de_tramite=row.values[9],
                    usuario=request.user.username,
                    timestamp=timestamp
                )


                try:
                    operation_type = OperationTypeModel.objects.get(id=str(row.values[8]))
                except OperationTypeModel.DoesNotExist:
                    operation_type = OperationTypeModel.objects.create(name=str(row.values[9]), id=str(row.values[8]))

                obj_sir.codigo_de_tramite = operation_type


                try:
                    obj_sir.fecha_de_pago = row.values[3].strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    obj_sir.fecha_de_pago = None


                try:
                    obj_sir.estado_en_sir = bool(row.values[4])
                except Exception:
                    obj_sir.estado_en_sir = None


                try:
                    obj_sir.cantidad_de_dominios = int(row.values[6])
                except Exception:
                    obj_sir.cantidad_de_dominios = None

                try:
                    obj_sir.numero_de_factura = int(row.values[10])
                except Exception:
                    obj_sir.numero_de_factura = None

                obj_sir.save()

                results['i'] += 1

            except IntegrityError as e:

                obj_sir = SIRModel.objects.get(transaccion=row.values[0])

                obj_sir.medio_de_pago = row.values[1]
                obj_sir.monto = row.values[2]
                obj_sir.dominio = row.values[5]
                obj_sir.cantidad_de_dominios = row.values[6]
                obj_sir.id_tad = row.values[7]
                #obj_sir.codigo_de_tramite_id = str(row.values[8])
                obj_sir.tipo_de_tramite = row.values[9]
                obj_sir.usuario = request.user.username

                try:
                    operation_type = OperationTypeModel.objects.get(id=str(row.values[8]))
                except OperationTypeModel.DoesNotExist:
                    operation_type = OperationTypeModel.objects.create(name=str(row.values[9]), id=str(row.values[8]))

                obj_sir.codigo_de_tramite = operation_type
                
                try:
                    obj_sir.fecha_de_pago = row.values[3].strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    obj_sir.fecha_de_pago = None

                try:
                    obj_sir.estado_en_sir = bool(row.values[4])
                except Exception:
                    obj_sir.estado_en_sir = None

                try:
                    obj_sir.cantidad_de_dominios = int(row.values[6])
                except Exception:
                    obj_sir.cantidad_de_dominios = None

                try:
                    obj_sir.numero_de_factura = int(row.values[10])
                except Exception:
                    obj_sir.numero_de_factura = None

                obj_sir.save()

                results['duplicate'] += 1


                
            except Exception as e:
                a = e
                logger.exception(e)
        return results

    def confirm_upload(self, timestamp):
        with connection.cursor() as cursor:
            cursor.execute("update raw_data_sir set confirmed=true where confirmed=false and timestamp='%s'" % timestamp)

        call_command('process_decidir_card_payments')
        call_command('process_decidir_pmc_payments')
        call_command('process_gire_payments')

    def cancel_upload(self, timestamp):

        with connection.cursor() as cursor:
            cursor.execute("delete from raw_data_sir where confirmed=false and timestamp='%s'" % timestamp)