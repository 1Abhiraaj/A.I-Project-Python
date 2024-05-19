import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia 
import pywhatkit as wk
import webbrowser
import os
import pyautogui
from time import sleep
import random
import smtplib

engine = pyttsx3.init('sapi5')#The Speech Application Programming Interface or SAPI is an API developed by Microsoft to allow the use of speech recognition and speech synthesis within Windows applications.
voices = engine.getProperty('voices')#api voices are approched print(voices[0].id)# printed the api voice of david
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 250)

def speak(audio):# argumrnt provided to speak the camond 
    engine.say(audio)
    engine.runAndWait()
    
def say(text):
    os.system(f'say "{text}"')

def Wishme():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    
    elif hour>=12 and  hour<18:
        speak("good Afternoon!")
    else:
        speak("Good Evening!")
        
    speak("I am  Jarvis Sir. Please tell me How may I halpe you")       

def takeCommand():
    '''It takes microphone input from the user and returns string ouptut'''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1 #seconds of non-speaking audio before a phrese is considerd complete and many threshold to be seen
        r.energy_threshold = 300# minimum audio energy to consider for recording
        audio = r.listen(source)#  Records a single phrase from ``source`` (an ``AudioSource`` instance) into an ``AudioData`` instance, which it returns.

        try:
            print("Recognizing....")
            query = r.recognize_google(audio, language='en-in')#Using google for voice recognition.
        # query = r.recognize_google(audio, language='hi-in')#Using google for voice recognition.
            print(f"user said: {query}\n")#User query will be printed.
        except Exception as e:
            #print(e)
            print("Say that againg please... ")#Say that again will be printed in case of improper voice 
            return "None"#User query will be printed.
        return query
    
dictapp = {"command prompt":"cmd","Word":"winword","Excel":"excel","Firefox":"Firefox","spyder":"spyder","PowerPoint":"powerpnt"}
    
def openappweb(query):
    
    if ".com" in query or ".co.in" in query or ".org" in query:
        query = query.replace("open","")
        query = query.replace("jarvis","")
        query = query.replace("launch","")
        query = query.replace(" ","")
        webbrowser.open(f"https://www.{query}")
        speak("Launching, sir")
    else:
        keys = list(dictapp.keys())
        for app in keys:
            if app in query:
                try:
                    print(f"Trying to open {dictapp[app]}")
                    os.system(f"start {dictapp[app]}")
                    speak(f"{app} opened")
                except Exception as e:
                    print(f"Failed to open {app}: {e}")
                    speak(f"Sorry, I couldn't open {app}")

def closeappweb(query):
    speak("Closing, sir")
    if "one tab" in query or "1 tab" in query:
        pyautogui.hotkey("ctrl", "w")
    elif "2 tab" in query:
        for _ in range(2):
            pyautogui.hotkey("ctrl", "w")
            sleep(0.5)
    elif "3 tab" in query:
        for _ in range(3):
            pyautogui.hotkey("ctrl", "w")
            sleep(0.5)
    elif "4 tab" in query:
        for _ in range(4):
            pyautogui.hotkey("ctrl", "w")
            sleep(0.5)
    elif "5 tab" in query:
        for _ in range(5):
            pyautogui.hotkey("ctrl", "w")
            sleep(0.5)
    else:
        keys = list(dictapp.keys())
        for app in keys:
            if app in query:
                try:
                    print(f"Trying to close {dictapp[app]}")
                    os.system(f"taskkill /f /im {dictapp[app]}.exe")
                    speak(f"{app} closed")
                except Exception as e:
                    print(f"Failed to close {app}: {e}")
                    speak(f"Sorry, I couldn't close {app}")
    
if __name__ == "__main__":
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I")
    Wishme()
    takeCommand()
    while True:
        if 1:
            query = takeCommand()#Converting user query into lower case
            #Logic for executing tasks based on query
            
            if "stop" in query or "bye" in query or "quit" in query:
                speak("Goodbye Sir, have a nice day!")
                break
           
            sites = [["just YouTube", "https://www.youtube.com"], ["GitHub", "https://www.github.com"], ["just Google", "https://www.google.com"], ["Online GDB", "https://www.onlinegdb.com/"]]
            for site in sites:
                if f"Open {site[0]}".lower() in query.lower():
                    say(f"Opening {site[0]} sir...")
                    webbrowser.open(site[1])
                    speak("Opening Sir")
      
            if 'wikipedia' in query: #if wikipedia found in the query then this block will be executed
                speak('Searching fROMWikipedia....')
                query = query.replace("wikipedia", "  ")
                results = wikipedia.summary(query, sentences=2)
                speak("According to wikipedia")
                print(results)
                speak(results)
                
            elif 'open Google' in query:
                    speak("What should I search ? ")
                    qry = takeCommand().lower()
                    url = f"https://www.google.com/search?q={qry}"
                    speak(f"Searching Google for {qry}")
                    webbrowser.open(url)
                                
            elif 'open YouTube' in query:
                speak("What should I search for on YouTube?")
                qry = takeCommand().lower()
                url = f"https://www.youtube.com/results?search_query={qry}"
                speak(f"Searching YouTube for {qry}")
                webbrowser.open(url)
                wk.playonyt(qry)
                speak("Here are the results, Sir")
            
            elif "open" in query:
                openappweb(query)
            elif "close" in query:
                closeappweb(query)
            
            elif 'play music' in query:
                music_dir = 'F:\SONG\A FOLDER'
                songs = os.listdir(music_dir)
                #print(songs)
                # Use random.choice() to select a random song from the list
                random_song = random.choice(songs)
                os.startfile(os.path.join(music_dir, random_song))
                speak("Opening sir")
            
            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")
                
            elif 'open camera' in query:
                try:
                    os.system("start microsoft.windows.camera:")  # Command to open the camera on Windows systems
                    speak("Opening camera")
                except Exception as e:
                    print(e)
                    speak("Sorry, I couldn't open the camera.")
        
            
            
            
