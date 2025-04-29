import speech_recognition as sr
import pyttsx3
import requests
import webbrowser
import os
import datetime
import random
import subprocess
import sys

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to listen to user input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return None

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
    music_dir = "C:/Users/Ali Haider/OneDrive/Music"  # Replace with your music directory
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
def open_website(url):
    webbrowser.open(url)
    speak(f"Opening {url}.")

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
    if "open " in command:
        website = command.split("open ")[1].strip()
        if not website.startswith(("http://", "https://")):
            website = f"https://www.{website}"
        try:
            webbrowser.open(website)
            print(f"Opening {website}")
        except Exception as e:
            print(f"Error opening website: {e}")
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
        exit()
    else:
        speak("Sorry, I don't know how to do that.")

# Main loop
if __name__ == "__main__":
    speak("Hello! I am your voice assistant. How can I help you?")
    while True:
        command = listen()
        if command:
            handle_command(command)

# Additional features can be added below
# Example: Add more commands, integrate with APIs, or connect to smart home devices.

# Function to check system information
def system_info():
    import platform
    system = platform.system()
    version = platform.version()
    speak(f"You are using {system} version {version}.")

# Function to open applications
def open_application(app_name):
    try:
        subprocess.Popen(app_name)
        speak(f"Opening {app_name}.")
    except Exception as e:
        speak(f"Sorry, I couldn't open {app_name}.")

# Function to check battery status (for laptops)
def check_battery():
    import psutil
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        speak(f"Your battery is at {percent} percent.")
    else:
        speak("Sorry, I couldn't check the battery status.")

# Function to send an email
def send_email():
    speak("Who should I send the email to?")
    recipient = listen()
    if recipient:
        speak("What is the subject?")
        subject = listen()
        if subject:
            speak("What should the message say?")
            message = listen()
            if message:
                try:
                    import smtplib
                    from email.mime.text import MIMEText
                    from email.mime.multipart import MIMEMultipart

                    # Replace with your email credentials
                    sender_email = "your_email@example.com"
                    sender_password = "your_password"

                    msg = MIMEMultipart()
                    msg["From"] = sender_email
                    msg["To"] = recipient
                    msg["Subject"] = subject
                    msg.attach(MIMEText(message, "plain"))

                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, recipient, msg.as_string())
                    server.quit()

                    speak("Email sent successfully.")
                except Exception as e:
                    speak("Sorry, there was an error sending the email.")
            else:
                speak("Sorry, I didn't get the message.")
        else:
            speak("Sorry, I didn't get the subject.")
    else:
        speak("Sorry, I didn't get the recipient.")