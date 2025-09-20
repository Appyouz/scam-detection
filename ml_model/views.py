from django.shortcuts import render

def home(request):
    return render(request, 'ml_model/index.html')
