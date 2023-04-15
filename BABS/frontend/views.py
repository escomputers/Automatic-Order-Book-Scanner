from django.shortcuts import render
from django_q.tasks import schedule
import json


def home(request):
    return render(request, 'home.html')


def addjobs(request):

    if request.method == 'POST':
        # Get ajax dictionary from frontend
        usrdata = json.loads(request.POST['data'])

        request.session['context'] = usrdata
        print(usrdata)


        # Assign task to DjangoQ
        # schedule('django.core.mail.send_mail', subject, msg, from_email, [currentuser.email], fail_silently=False, html_message=html_content, evento_calendar=eventID, schedule_type=Schedule.ONCE, next_run=delta, cluster='DjangORMcalendar')


    return render(request, 'add-jobs.html')
