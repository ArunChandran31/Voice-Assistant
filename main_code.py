import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser  
import re
import requests
from math import *
import random

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
print(voices[0].id)
engine.setProperty('voice',voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour <12:
        speak("Hello. Good morning")

    elif hour>=12 and hour<18:
        speak("Hello. Good afternoon")

    else:
        speak("Hello. Good evening")
    speak("I am JARVIS. your personal A I assistant. How can i help you.")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1)
        r.pause_threshold=1
        print("Listening..")
        audio=r.listen(source)

    try:
        query= r.recognize_google(audio)
        print(f"You said: {query}\n")

    except Exception as e:
        print("Can you please say again sir..")
        return 'None'
    return query
        
def set_alarm(alarm_time):
    speak(f"Setting alarm for {alarm_time}")
    alarm_hour, alarm_minute = map(int, alarm_time.split(':'))
    while True:
        if datetime.datetime.now().hour == alarm_hour and datetime.datetime.now().minute == alarm_minute:
            speak("Wake up! It's time.")
            break
        time.sleep(60)

def set_timer(timer_minutes):
    speak(f"Setting timer for {timer_minutes} minutes")
    timer_seconds = int(timer_minutes) * 60
    time.sleep(timer_seconds)
    speak(f"The timer for {timer_minutes} minutes is up!")

def convert_units(value, from_unit, to_unit):
    conversion_table = {
        'meters': {'meters': lambda x: x, 'kilometers': lambda x: x / 1000, 'centimeters': lambda x: x * 100,
                   'millimeters': lambda x: x * 1000, 'inches': lambda x: x * 39.3701, 'feet': lambda x: x * 3.28084,
                   'yards': lambda x: x * 1.09361, 'miles': lambda x: x / 1609.34},
        'kilometers': {'meters': lambda x: x * 1000, 'kilometers': lambda x: x, 'centimeters': lambda x: x * 100000,
                       'millimeters': lambda x: x * 1000000, 'inches': lambda x: x * 39370.1,
                       'feet': lambda x: x * 3280.84, 'yards': lambda x: x * 1093.61, 'miles': lambda x: x / 1.60934},
        'centimeters': {'meters': lambda x: x / 100, 'kilometers': lambda x: x / 100000,
                        'centimeters': lambda x: x, 'millimeters': lambda x: x * 10, 'inches': lambda x: x / 2.54,
                        'feet': lambda x: x / 30.48, 'yards': lambda x: x / 91.44, 'miles': lambda x: x / 160934},
        'millimeters': {'meters': lambda x: x / 1000, 'kilometers': lambda x: x / 1000000,
                        'centimeters': lambda x: x / 10, 'millimeters': lambda x: x, 'inches': lambda x: x / 25.4,
                        'feet': lambda x: x / 304.8, 'yards': lambda x: x / 914.4, 'miles': lambda x: x / 1.609e+6},
        'inches': {'meters': lambda x: x * 0.0254, 'kilometers': lambda x: x * 2.54e-5,
                   'centimeters': lambda x: x * 2.54, 'millimeters': lambda x: x * 25.4, 'inches': lambda x: x,
                   'feet': lambda x: x / 12, 'yards': lambda x: x / 36, 'miles': lambda x: x / 63360},
        'feet': {'meters': lambda x: x * 0.3048, 'kilometers': lambda x: x * 3.048e-4,
                 'centimeters': lambda x: x * 30.48, 'millimeters': lambda x: x * 304.8, 'inches': lambda x: x * 12,
                 'feet': lambda x: x, 'yards': lambda x: x / 3, 'miles': lambda x: x / 5280},
        'yards': {'meters': lambda x: x * 0.9144, 'kilometers': lambda x: x * 9.144e-4,
                  'centimeters': lambda x: x * 91.44, 'millimeters': lambda x: x * 914.4, 'inches': lambda x: x * 36,
                  'feet': lambda x: x * 3, 'yards': lambda x: x, 'miles': lambda x: x / 1760},
        'miles': {'meters': lambda x: x * 1609.34, 'kilometers': lambda x: x * 1.60934,
                  'centimeters': lambda x: x * 160934, 'millimeters': lambda x: x * 1.609e+6,
                  'inches': lambda x: x * 63360, 'feet': lambda x: x * 5280, 'yards': lambda x: x * 1760,
                  'miles': lambda x: x}
    }
    try:
        result = conversion_table[from_unit][to_unit](value)
        return result
    except KeyError:
        return None

if __name__=="__main__":
    wishMe()
    while True:
        query=takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia..')
            query=query.replace("wikipedia","")
            results=wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'the time' in query:
            strTime=datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {strTime}")

        elif 'weather' in query:
            speak('Specify your location?')
            search = takeCommand()
            url = f"https://www.google.com/search?q=weather+in+{search}"
            webbrowser.get().open(url)
            speak(f"Sure.")

        elif 'set alarm' in command:
            speak("At what time should I set the alarm?")
            alarm_time = takeCommand()
            set_alarm(alarm_time)
        
        elif 'set timer' in command:
            speak("For how many minutes should I set the timer for?")
            timer_minutes = takeCommand()
            set_timer(timer_minutes)
        
        elif 'calculate' in command:
            calculation = re.search(r'\d+(\s+\+|\s*\-|\s*\*|\s*/\s*)\d+', command)
            if calculation:
                result = eval(calculation.group(0))
                speak(f"The result is {result}")
            else:
                speak("Sorry, I couldn't understand the calculation.")
    
        elif 'convert' in command:
            conversion = re.search(r'\d+\s*(\w+)\s+to\s+(\w+)', command)
            if conversion:
                value, from_unit, to_unit = conversion.groups()
                result = convert_units(float(value), from_unit, to_unit)
                if result:
                    speak(f"{value} {from_unit} is equal to {result} {to_unit}")
                else:
                    speak("Sorry, I couldn't perform the conversion.")
            else:
                speak("Sorry, I couldn't understand the conversion.")

        elif 'quit' in query:
            def goodbye():
                hour=int(datetime.datetime.now().hour)
                if (hour>=0 and hour <12) or (hour>=12 and hour<18):
                    speak("Goodbye!")
                else:
                    speak("Good Night.")

            goodbye()   
            break
