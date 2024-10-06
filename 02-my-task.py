import speech_recognition as sr
import pyttsx3
import requests
from datetime import datetime

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen and recognize voice input
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query.lower()
        except Exception as e:
            print("Sorry, I didn't catch that. Please try again.")
            return None

# Task Management (To-Do List)
tasks = []

def add_task(task):
    tasks.append(task)
    speak(f"Task '{task}' added to your list.")

def list_tasks():
    if tasks:
        speak("Your tasks are:")
        for i, task in enumerate(tasks, 1):
            speak(f"{i}. {task}")
    else:
        speak("Your task list is empty.")

# Weather Updates (using OpenWeatherMap API)
def get_weather(city_name):
    api_key = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(base_url)
        weather_data = response.json()

        if weather_data["cod"] != "404":
            main = weather_data["main"]
            temperature = main["temp"]
            weather_description = weather_data["weather"][0]["description"]
            speak(f"The temperature in {city_name} is {temperature} degrees Celsius with {weather_description}.")
        else:
            speak(f"City {city_name} not found.")
    except Exception as e:
        speak("Unable to retrieve weather information at the moment.")

# Smart Home Device Integration (Example - Basic Light Control)
def control_light(action):
    if action == "on":
        # Simulate turning the light on
        speak("Turning the lights on.")
    elif action == "off":
        # Simulate turning the light off
        speak("Turning the lights off.")
    else:
        speak("Sorry, I can only turn the lights on or off.")

# Core function to handle tasks
def handle_query(query):
    if 'hello' in query:
        speak("Hello! How can I assist you today?")
    elif 'your name' in query:
        speak("I am your custom voice assistant.")
    elif 'time' in query:
        now = datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {now}")
    
    # Task Management
    elif 'add task' in query:
        task = query.replace('add task', '').strip()
        if task:
            add_task(task)
        else:
            speak("Please specify a task to add.")
    elif 'list tasks' in query:
        list_tasks()

    # Weather Updates
    elif 'weather' in query:
        city = query.replace('weather in', '').strip()
        if city:
            get_weather(city)
        else:
            speak("Please specify a city.")

    # Smart Home Light Control
    elif 'turn light' in query:
        if 'on' in query:
            control_light('on')
        elif 'off' in query:
            control_light('off')
        else:
            speak("Please specify whether to turn the light on or off.")

    # Unknown command
    else:
        speak("I'm still learning. Let me know if you need anything else.")

# Main loop to keep the assistant active
if __name__ == "__main__":
    speak("Welcome! I'm ready to assist you.")
    while True:
        query = listen()
        if query:
            handle_query(query)
