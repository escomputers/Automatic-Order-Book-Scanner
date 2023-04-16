from django.shortcuts import render
from django_q.tasks import schedule, Schedule
import json
from django_q.models import Schedule


def home(request):
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
            element = {'symbol': symbol, 
                       'next_run': next_run,
                       'interval': interval, 
                       'grouping': grouping, 
                       'depth': depth
            }
            context.append(element)
    except Schedule.DoesNotExist:
        context = None


    return render(request, 'home.html', context={'tasks': context})


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
