import datetime
from django.db import connection

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        try:

            payment_method = 'Pago Mis Cuentas'

            with connection.cursor() as cursor:
                cursor.execute(("select sum(monto) from conciliacion where year(fecha_de_pago) = year(current_date  - interval 1 month) AND MONTH(fecha_de_pago) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH) AND medio_de_pago='%s';") % (payment_method))
                result = cursor.fetchone()

                try:

                    cursor.execute(("select count(*) from results where month = %d and year = %d and payment_method='%s'") % ((datetime.datetime.today() - datetime.timedelta(days=30)).month, (datetime.datetime.today() - datetime.timedelta(days=30)).year, payment_method))
                    count = cursor.fetchone()
                    if count[0] > 0:
                        cursor.execute(("UPDATE results SET amount = %f where month = %d and year = %d and payment_method='%s'") % (
                                        result[0],
                                       (datetime.datetime.today() - datetime.timedelta(days=30)).month,
                                       (datetime.datetime.today() - datetime.timedelta(days=30)).year,
                                       payment_method))
                    else:
                        cursor.execute(("INSERT INTO results (month, year, amount, payment_method) VALUES ('%s', '%s', %f, '%s')") % (
                                       (datetime.datetime.today() - datetime.timedelta(days=30)).month,
                                       (datetime.datetime.today() - datetime.timedelta(days=30)).year, result[0],
                                       payment_method))

                except Exception as e:
                    pass

        except Exception as e:
            a=e
