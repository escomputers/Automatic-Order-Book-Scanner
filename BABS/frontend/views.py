from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def addjobs(request):
    return render(request, 'add-jobs.html')
