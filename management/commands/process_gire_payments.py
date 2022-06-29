from django.db import connection

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        try:
            c = 0
            with connection.cursor() as cursor:
                cursor.execute("SELECT rs.transaccion, rs.medio_de_pago, rs.monto, rs.id_tad, rs.fecha_de_pago, rs.dominio, rs.codigo_de_tramite_id, rs.numero_de_factura, rs.estado_en_sir FROM raw_data_gire rg INNER JOIN raw_data_sir rs ON (rg.barcode=rs.transaccion) WHERE rg.matched=false and rs.estado_en_sir=true;")
                objects = cursor.fetchall()
                if len(objects) == 0:
                   self.stdout.write(self.style.SUCCESS('No se han encontrado registros para procesar GIRE'))
                else:
                    self.stdout.write(self.style.SUCCESS(str(len(objects)) + ' registros para procesar GIRE')) 
                    for i in objects:
                        try:

                            lista = list(i)

                            if lista[4] == None: 
                                datetime_str = 'NULL'
                            else:
                                datetime_str = "'" + lista[4].strftime('%Y-%m-%d %H:%M:%S') + "'"


                            cursor.execute(("INSERT INTO conciliacion (transaccion, medio_de_pago, monto, id_tad, fecha_de_pago, dominios, codigo_de_tramite_id, numero_de_factura, estado_en_sir) VALUES ('%s', '%s', %f, '%d', %s, '%s', '%s', '%s', '%s')") % (lista[0], lista[1], lista[2], int(lista[3]), datetime_str, lista[5], lista[6], lista[7], lista[8] ))
                            cursor.execute(("UPDATE raw_data_gire SET matched=true WHERE barcode='%s'" % i[0]) )
                            cursor.execute(("UPDATE raw_data_sir SET matched=true WHERE transaccion='%s'" % i[0]))

                            c += 1
                        except Exception as e:
                            pass

                    if c > 0:
                        self.stdout.write(self.style.SUCCESS(
                            '%s - %s registros procesados GIRE' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), c)))
        except Exception as e:
            print(e)
            a=e