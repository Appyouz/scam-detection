import joblib
import re
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .feature_extractor import get_url_features

url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

# load the trained model once when the server starts
# Handle cases where the file might not exist
try:
    model_path  = 'ml_model/data/scam_detector_model.pkl'
    loaded_model = joblib.load(model_path)
    print("Model loaded successfully!")
except FileNotFoundError:
    print(f"Error: The model file was not found at {model_path}")
    loaded_model = None


@csrf_exempt
def home(request):
    """
    Renders the home page
    """
    return render(request, 'ml_model/index.html')


@csrf_exempt
def prediction_view(request):
    """
    Handles the API request, gets the email text, and returns a dummy JSON response.
    """
    # Check that the request method is POST
    if request.method  == "POST":
        # Check if model failed to load
        if loaded_model is None:
            return JsonResponse({"result": "Error: ML model not found."}, status=500)
        try:
            # Parse the incoming JSON data from the request body
            data = json.loads(request.body.decode("utf-8"))
            email_text = data.get("email_text", "")
            print(email_text)

            # Find the first url in the email text
            found_url =  url_pattern.search(email_text)

            if not found_url:
                result = "Safe"
                return JsonResponse({"result": result})

            # if url is found need to pass it to feature extractor
            url_to_analyze = found_url.group(0)
            print(f"URL found: {url_to_analyze}")

            # Most important part: use feature extractor to get numercal values from the URL
            features = get_url_features(url_to_analyze)

            # Make a prediction using the loaded model
            prediction = loaded_model.predict([features])

            # Convert the prediction(0 or 1) to human-readable string
            if prediction[0] == 1:
                result = "Malicious"
            else:
                result = "Safe"

            return JsonResponse({"result": result})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            # Catch any other unexpected errors and return a clear message.
            print(f"An error occurred during prediction: {e}")
            return JsonResponse({"result": "Error during prediction."}, status=500)


    return JsonResponse({"error": "Invalid request method"}, status=405)
