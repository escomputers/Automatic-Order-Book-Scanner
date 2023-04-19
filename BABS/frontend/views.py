from django.shortcuts import render, get_object_or_404
from django_q.tasks import schedule, Schedule
import json
from django.http import JsonResponse
from django_q.models import Schedule
from frontend.models import ScanResults



from django.db.models import Max


def home(request):
    '''
    try:
        context = []
        tasks = Schedule.objects.all().values()
        for i in tasks:
            objects_names = i.get('name')
            values = objects_names.split('-')
            symbol = values[0]
            interval = values[1]
            grouping = values[2]
            depth = values[3]
            next_run = i.get('next_run')
            id = i.get('id')
            element = {'id': id,
                    'symbol': symbol, 
                    'next_run': next_run,
                    'interval': interval, 
                    'grouping': grouping, 
                    'depth': depth
            }
            context.append(element)
    '''
    # except Schedule.DoesNotExist:
    rows = ScanResults.objects.all().values()
    for row in rows:
        asks_row = []
        bids_row = []
        for price, values in row['asks'].items():
            asks_row.append({'x': price, 'y': values['QTY']})
        #for price, values in row['bids'].items():
        #    bids_row.append({'x': price, 'y': values['QTY']})
        #asks.append(asks_row)
        #bids.append(bids_row)
        context = json.dumps(asks_row)
        # context = {'x': price, 'y': values['QTY']}


    return render(request, 'home.html', context={'context': context}) # , context={'tasks': context}


def addtasks(request):
    if request.method == 'POST':
        # Get ajax dictionary from frontend
        usrdata = json.loads(request.POST['data'])

        request.session['context'] = usrdata

        name = usrdata['pair'] + '-' + \
            usrdata['refreshinterval'] + '-' + \
            usrdata['grouping'] + '-' + \
            usrdata['depth']

        # Assign task to DjangoQ
        schedule('frontend.utils.Scan',
            usrdata['pair'], usrdata['grouping'], usrdata['depth'],
            name=name,
            schedule_type=Schedule.MINUTES, 
            minutes=int(usrdata['refreshinterval']),
            repeats=-1
        )


    return render(request, 'add-tasks.html')


def deletetasks(request):
    # Get ajax variable containing task_id to be removed
    id = json.loads(request.POST['data'])

    # Delete task object
    task_object = get_object_or_404(Schedule, pk = id)
    task_object.delete()


    return render(request, 'home.html')


def chartview(request):
    try:
        db_objects = ScanResults.objects.all()

        return JsonResponse({'data': list(db_objects.values())})
    except ScanResults.DoesNotExist:
        return JsonResponse({'data': None})