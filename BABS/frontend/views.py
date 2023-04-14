from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def jobs(request):
    return render(request, 'jobs.html')
