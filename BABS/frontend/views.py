from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django_q.tasks import schedule, Schedule
import json
from django_q.models import Schedule
from frontend.models import ScanResults, Symbol
from collections import Counter

def tasks(request):
    try:
        context = []
        tasks = Schedule.objects.all().values()
        for i in tasks:
            if i['name'] != 'job-update-symbols':
                next_run = i.get('next_run')
                id = i.get('id')

                # Construct name from schedule name
                objects_names = i.get('name')
                values = objects_names.split('-')
                symbol = values[0]
                interval = values[1]
                grouping = values[2]
                depth = values[3]

                last_task = Schedule.objects.get(name=objects_names)
                last_status = last_task.success()

                element = {'id': id,
                        'symbol': symbol, 
                        'next_run': next_run,
                        'interval': interval, 
                        'grouping': grouping, 
                        'depth': depth,
                        'status': last_status
                }
                context.append(element)

    except IndexError:
        context = None

    if request.method == 'POST':
        # Get ajax dictionary from frontend
        usrdata = json.loads(request.POST['data'])

        #request.session['context'] = usrdata

        name = usrdata['pair'] + '-' + \
            usrdata['refreshinterval'] + '-' + \
            usrdata['grouping'] + '-' + \
            usrdata['depth']

        tasks = Schedule.objects.all().values()
        for i in tasks:
            if i['name'] != 'job-update-symbols':
                if i['name'] == name:
                    return JsonResponse({'success': False})
                else:
                    # Assign task to DjangoQ
                    schedule('frontend.utils.Scan',
                        usrdata['pair'], usrdata['grouping'], usrdata['depth'],
                        name=name,
                        schedule_type=Schedule.MINUTES, 
                        minutes=int(usrdata['refreshinterval']),
                        repeats=-1
                    )
                    return JsonResponse({'success': True})


    return render(request, 'tasks.html', context={'tasks': context})


def deletetasks(request):
    # Get ajax variable containing task_id to be removed
    id = json.loads(request.POST['data'])

    # Delete task object
    task_object = get_object_or_404(Schedule, pk = id)
    task_object.delete()


    return render(request, 'home.html')


def symbolchart(request, symbol_id):
    asksjson = None # empty columns case
    bidsjson = None

    symbol = Symbol.objects.get(pk=symbol_id)
    # rows = ScanResults.objects.all().values()
    rows = ScanResults.objects.filter(symbol=symbol).order_by('timestamp').values()
    for row in rows:
        asks_row = []
        bids_row = []

        asks_dict = json.loads(row['asks'])
        bids_dict = json.loads(row['bids'])

        for price, values in asks_dict.items():
            asks_row.append({'x': price, 'y': values['QTY']})
        for price, values in bids_dict.items():
            bids_row.append({'x': price, 'y': values['QTY']})

        asksjson = json.dumps(asks_row)
        bidsjson = json.dumps(bids_row)
        timestamps = row['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')


    return render(request, 'symbol_chart.html', context={'symbol': symbol, 'asks': asksjson, 'bids': bidsjson, 'timestamps': timestamps})


def symbols(request):
    pairs = Symbol.objects.all().values()
    symbols = []
    for pair in pairs:
        symbols.append(pair)


    return JsonResponse({'symbols': symbols})


def charts(request):
    try:
        # Get all symbols ids having ScanResults
        rows = ScanResults.objects.all().values()
        symbol_ids = []
        for row in rows:
            symbol_ids.append(row['symbol_id'])

        counted_lst = Counter(symbol_ids)

        for k, v in counted_lst.items():
            symbols_objects = Symbol.objects.get(pk=k)
            symbols = {'id': k, 'symbol': str(symbols_objects), 'counts': v}
    except ScanResults.DoesNotExist:
        symbols = None


    return render(request, 'charts.html', context={'symbols': symbols})