import os
import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

# NOTE: Replace with your Gemini API key.
# It is highly recommended to use environment variables for keys in a real project.
GEMINI_API_KEY =  os.getenv("GEMINI_API_KEY")
print("API KEY:", GEMINI_API_KEY)  # <-- check what prints here

def index(request):
    """
    Renders the main chat application page.
    """
    return render(request, 'chatbot/index.html')

@csrf_exempt
def get_gemini_response(request):
    """
    Handles POST requests from the frontend to get a response from the Gemini API.
    """
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            user_message = data.get('message')

            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)

            # Construct the payload for the Gemini API
            payload = {
                "contents": [
                    {"parts": [{"text": user_message}]}
                ]
            }
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}"

            # Send the request to the Gemini API
            response = requests.post(
                api_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            # Check for a successful response and extract the text
            if response.status_code == 200:
                response_data = response.json()
                gemini_text = response_data['candidates'][0]['content']['parts'][0]['text']
                return JsonResponse({'response': gemini_text})
            else:
                return JsonResponse(
                    {'error': 'Gemini API call failed', 'details': response.text},
                    status=response.status_code
                )

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
