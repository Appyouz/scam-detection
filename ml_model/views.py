from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def home(request):
    if request.method == 'POST':
        input_text = request.POST.get('email-text', '')
        print("Received text for analysis: ",  input_text)

        # ML model prediction logic goes here

    return render(request, 'ml_model/index.html')
