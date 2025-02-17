from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import TodoItem
import requests
import google.generativeai as genai
import json


genai.configure(api_key="enter your api key here ")   #genrate api key through google cloud for fetching data from gemini

def chatbot_ui(request):
    return render(request, 'chatbot/chat.html')

def chatbot_response(request):
    if request.method == 'POST':
        try:
            # Debugging: Print incoming request body for better debugging
            print("Incoming POST data:", request.body.decode('utf-8'))

            # Parse the JSON data from the request body
            body = json.loads(request.body.decode('utf-8'))

            # Get the user message from the body (it should be part of the JSON)
            user_message = body.get('message', None)

            # Debugging: Print the extracted message
            print(f"Extracted user message: {user_message}")

            # Check if message is provided
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)

            # Call the Gemini API
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_message)
            response_message = response.text

            # Debugging: Print the bot's response before sending it to the frontend
            print(f"Generated response from Gemini API: {response_message}")

            return JsonResponse({'response': response_message})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            # Debugging: Catch and print any other errors
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': f"API Error: {str(e)}"}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)



# Weather and To-Do
def weather(request):
    city = request.GET.get('city', 'Toronto')
    api_key = '86d5c5c3534874ba0610c2ecf52a2a0d'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    context = {'city': city}
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            context.update({
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'feels_like': data['main']['feels_like'],
                'icon': data['weather'][0]['icon'],
            })
    except requests.RequestException:
        pass

    tasks = TodoItem.objects.all()
    if request.method == "POST":
        task = request.POST.get('task')
        if task:
            TodoItem.objects.create(task=task)
        return redirect('weather')

    context['tasks'] = tasks

   
    return render(request, 'wtc1app/weather.html', context)
# Delete Task
def delete_task(request, task_id):
    TodoItem.objects.filter(id=task_id).delete()
    return redirect('weather')
