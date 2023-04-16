from django.shortcuts import render
from django_q.tasks import schedule, Schedule
import json


def home(request):
    return render(request, 'home.html')


def addjobs(request):
    if request.method == 'POST':
        # Get ajax dictionary from frontend
        usrdata = json.loads(request.POST['data'])

        request.session['context'] = usrdata

        name = usrdata['pair'] + '-' + \
            'I' + usrdata['refreshinterval'] + '-' + \
            'G' + usrdata['grouping'] + '-' + \
            'D' + usrdata['depth']

        # Assign task to DjangoQ
        schedule('modules.scan', usrdata['pair'], usrdata['grouping'], 
            usrdata['depth'], name=name,
            schedule_type=Schedule.MINUTES, 
            minutes=int(usrdata['refreshinterval'])
        )


    return render(request, 'add-jobs.html')
