import csv

class Utils:
    
    @staticmethod
    def export_csv(request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="file.csv"'
        conciliaciones = ConciliacionModel.objects.all()
        writer = csv.writer(response)
        for conciliacion in conciliaciones:
            writer.writerow(conciliacion)
        return response

    @staticmethod
    def validate_empty_file(request):

        if not request.FILES:
            raise Exception('Debe ingresar un archivo')

    @staticmethod
    def get_query(request):
        query = ''
        for r in request.GET:
            if r != 'page':
                if query:
                    query = query + '&'
                query = query + r + '=' + request.GET[r]

        return query

    @staticmethod
    def get_paginator_dict(paginator, page_number):
        paginator_dict = []
        if paginator.paginator.num_pages > 15:

            if (page_number - 5) <= 0:

                for i in range(1, 10):
                    paginator_item = {}
                    paginator_item['i'] = i
                    paginator_dict.append(paginator_item)
                paginator_item = {}
                paginator_item['disabled'] = True
                paginator_item['i'] = '...'
                paginator_dict.append(paginator_item)
                paginator_item = {}
                paginator_item['i'] = paginator.paginator.num_pages
                paginator_dict.append(paginator_item)
            elif (page_number + 5) > paginator.paginator.num_pages:
                paginator_item = {}
                paginator_item['i'] = 1
                paginator_dict.append(paginator_item)
                paginator_item = {}
                paginator_item['disabled'] = True
                paginator_item['i'] = '...'
                paginator_dict.append(paginator_item)
                for i in range(paginator.paginator.num_pages - 10, paginator.paginator.num_pages + 1):
                    paginator_item = {}
                    paginator_item['i'] = i
                    paginator_dict.append(paginator_item)
            else:
                paginator_item = {}
                paginator_item['i'] = 1
                paginator_dict.append(paginator_item)
                paginator_item = {}
                paginator_item['disabled'] = True
                paginator_item['i'] = '...'
                paginator_dict.append(paginator_item)
                for i in range(page_number - 5, page_number + 5):
                    if i != 1:
                        paginator_item = {}
                        paginator_item['i'] = i
                        paginator_dict.append(paginator_item)
                paginator_item = {}
                paginator_item['disabled'] = True
                paginator_item['i'] = '...'
                paginator_dict.append(paginator_item)
                paginator_item = {}
                paginator_item['i'] = paginator.paginator.num_pages
                paginator_dict.append(paginator_item)
        else:
            for i in range(1, paginator.paginator.num_pages + 1):
                paginator_item = {}
                paginator_item['i'] = i
                paginator_dict.append(paginator_item)

        return paginator_dict