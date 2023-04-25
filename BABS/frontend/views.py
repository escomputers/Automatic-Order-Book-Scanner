from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django_q.tasks import schedule, Schedule
import json
from django_q.models import Schedule
from frontend.models import ScanResults, Symbol


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


def charts(request):
    asksjson = None # empty columns case
    bidsjson = None

    rows = ScanResults.objects.all().values()
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


    return render(request, 'charts.html', context={'asks': asksjson, 'bids': bidsjson})


def symbols(request):
    pairs = Symbol.objects.all().values()
    symbols = []
    for pair in pairs:
        symbols.append(pair)


    return JsonResponse({'symbols': symbols})