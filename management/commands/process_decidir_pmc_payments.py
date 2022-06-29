from django.db import connection
import datetime
from django.core.management.base import BaseCommand
from datetime import datetime

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        try:
            c = 0
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT rs.transaccion, rs.medio_de_pago, rs.monto, rs.id_tad, rs.fecha_de_pago, rs.dominio, rs.codigo_de_tramite_id, rs.numero_de_factura, rs.estado_en_sir FROM raw_data_decidir_pmc rd INNER JOIN raw_data_sir rs ON (rd.id_operacion=rs.transaccion) WHERE rd.matched=false and rs.estado_en_sir=true;")
                objects = cursor.fetchall()
                
                if len(objects) == 0:
                   self.stdout.write(self.style.SUCCESS('No se han encontrado registros para procesar PMC'))
                else:
                    self.stdout.write(self.style.SUCCESS(str(len(objects)) + ' registros para procesar PMC'))    
                    for i in objects:
                        
                        try:
                            lista = list(i)

                            if lista[4] == None: 
                                datetime_str = 'NULL'
                            else:
                                datetime_str = "'" + lista[4].strftime('%Y-%m-%d %H:%M:%S') + "'"


                            cursor.execute(("INSERT INTO conciliacion (transaccion, medio_de_pago, monto, id_tad, fecha_de_pago, dominios, codigo_de_tramite_id, numero_de_factura, estado_en_sir) VALUES ('%s', '%s', %f, '%d', %s, '%s', '%s', '%s', '%s')") % (lista[0], lista[1], lista[2], int(lista[3]), datetime_str, lista[5], lista[6], lista[7], lista[8] ))
                            cursor.execute(("UPDATE raw_data_decidir_pmc SET matched=true WHERE id_operacion='%s'" % lista[0]) )
                            cursor.execute(("UPDATE raw_data_sir SET matched=true WHERE transaccion='%s'" % lista[0]))

                            c += 1
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(str(len(objects)) + ' error para procesar PMC en la transacción ' + lista[0]))    
                            print(e)
                            pass
                    
                    if c > 0:
                        self.stdout.write(self.style.SUCCESS(
                            '%s - %s registros procesados PMC' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), c)))
        except Exception as e:
            print(e)
            a=e

