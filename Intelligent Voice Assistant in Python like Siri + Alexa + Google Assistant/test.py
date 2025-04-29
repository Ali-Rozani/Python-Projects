import speech_recognition as sr
import pyttsx3
import requests
import webbrowser
import os
import datetime
import random
import tkinter as tk
from tkinter import ttk, scrolledtext
from threading import Thread
import sys

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()
    update_ui(f"Assistant: {text}")

# Function to update the UI with messages
def update_ui(message):
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, message + "\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)

# Function to listen to user input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        update_ui("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            update_ui(f"You: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return None

# Function to detect the wake word
def detect_wake_word():
    recognizer = sr.Recognizer()
    wake_word = "hey assistant"  # Change this to your preferred wake word
    while True:
        with sr.Microphone() as source:
            print("Waiting for wake word...")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio).lower()
                if wake_word in text:
                    speak("How can I help you?")
                    return True
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                speak("Sorry, my speech service is down.")
                return False

# Function to get weather information
def get_weather(city="New York"):
    api_key = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url).json()
        if response.get("weather"):
            weather = response["weather"][0]["description"]
            temperature = response["main"]["temp"]
            speak(f"The weather in {city} is {weather} with a temperature of {temperature} degrees Celsius.")
        else:
            speak("Sorry, I couldn't fetch the weather information.")
    except Exception as e:
        speak("Sorry, there was an error fetching the weather.")

# Function to play music
def play_music():
    music_dir = "C:/Music"  # Replace with your music directory
    if os.path.exists(music_dir) and os.path.isdir(music_dir):
        songs = [song for song in os.listdir(music_dir) if song.endswith(".mp3")]
        if songs:
            song = random.choice(songs)
            os.startfile(os.path.join(music_dir, song))
            speak(f"Playing {song}.")
        else:
            speak("No music files found in the directory.")
    else:
        speak("The specified music directory does not exist.")

# Function to open websites
def open_website(command):
    if "open " in command:
        # Extract website name and add standard prefix
        website = command.split("open ")[1].strip()
        if not website.startswith(("http://", "https://")):
            website = f"https://www.{website}"
        
        try:
            webbrowser.open(website)
            speak(f"Opening {website}.")
        except Exception as e:
            speak(f"Sorry, I couldn't open {website}.")

# Function to tell the time
def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current_time}.")

# Function to tell a joke
def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't skeletons fight each other? They don't have the guts.",
    ]
    joke = random.choice(jokes)
    speak(joke)

# Function to search the web
def search_web(query):
    try:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        speak(f"Here are the search results for {query}.")
    except Exception as e:
        speak("Sorry, I couldn't perform the search.")

# Function to set a reminder
def set_reminder():
    speak("What should I remind you about?")
    reminder = listen()
    if reminder:
        speak("In how many minutes?")
        try:
            minutes = int(listen())
            seconds = minutes * 60
            speak(f"Reminder set for {minutes} minutes.")
            import time
            time.sleep(seconds)
            speak(f"Reminder: {reminder}")
        except ValueError:
            speak("Sorry, I didn't understand the time.")

# Function to shut down the system
def shutdown_system():
    speak("Shutting down the system.")
    if sys.platform == "win32":
        os.system("shutdown /s /t 1")
    elif sys.platform == "linux" or sys.platform == "darwin":
        os.system("shutdown -h now")

# Function to handle commands
def handle_command(command):
    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you?")
    elif "weather" in command:
        if "in" in command:
            city = command.split("in")[-1].strip()
            get_weather(city)
        else:
            get_weather()
    elif "play music" in command:
        play_music()
    elif "open " in command:
        open_website(command)
    elif "time" in command:
        tell_time()
    elif "joke" in command:
        tell_joke()
    elif "search" in command:
        query = command.replace("search", "").strip()
        if query:
            search_web(query)
        else:
            speak("What would you like me to search for?")
            query = listen()
            if query:
                search_web(query)
    elif "reminder" in command:
        set_reminder()
    elif "shutdown" in command:
        shutdown_system()
    elif "exit" in command or "bye" in command:
        speak("Goodbye!")
        root.quit()
    else:
        speak("Sorry, I don't know how to do that.")

# Function to start listening in a separate thread
def start_listening():
    while True:
        if detect_wake_word():
            command = listen()
            if command:
                handle_command(command)

# Function to handle button clicks
def on_button_click(action):
    if action == "listen":
        Thread(target=start_listening).start()
    elif action == "weather":
        Thread(target=get_weather).start()
    elif action == "time":
        Thread(target=tell_time).start()
    elif action == "joke":
        Thread(target=tell_joke).start()
    elif action == "exit":
        speak("Goodbye!")
        root.quit()

# Create the main UI window
root = tk.Tk()
root.title("Intelligent Voice Assistant")
root.geometry("600x500")
root.configure(bg="#f0f0f0")

# Chat area to display conversation
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, width=70, height=20, bg="#ffffff", fg="#000000")
chat_area.pack(pady=10, padx=10)

# Buttons for common commands
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

listen_button = ttk.Button(button_frame, text="🎤 Listen", command=lambda: on_button_click("listen"))
listen_button.grid(row=0, column=0, padx=5)

weather_button = ttk.Button(button_frame, text="🌤️ Weather", command=lambda: on_button_click("weather"))
weather_button.grid(row=0, column=1, padx=5)

time_button = ttk.Button(button_frame, text="⏰ Time", command=lambda: on_button_click("time"))
time_button.grid(row=0, column=2, padx=5)

joke_button = ttk.Button(button_frame, text="😂 Joke", command=lambda: on_button_click("joke"))
joke_button.grid(row=0, column=3, padx=5)

exit_button = ttk.Button(button_frame, text="🚪 Exit", command=lambda: on_button_click("exit"))
exit_button.grid(row=0, column=4, padx=5)

# Start the main loop
speak("Hello! I am your voice assistant. Say 'Hey Assistant' to activate me.")
root.mainloop()