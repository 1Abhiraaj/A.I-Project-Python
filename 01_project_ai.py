import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia 
import pywhatkit as wk
import webbrowser
import os
import openai
from config import apikey
import pyautogui
from time import sleep
import random
import smtplib

engine = pyttsx3.init('sapi5')#The Speech Application Programming Interface or SAPI is an API developed by Microsoft to allow the use of speech recognition and speech synthesis within Windows applications.

voices = engine.getProperty('voices')#api voices are approched print(voices[0].id)# printed the api voice of david
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 200)

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

chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Harry: {query}\n Jarvis: "
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]
    
def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # todo: Wrap this inside of a  try catch block
        # print(response["choices"][0]["text"])
        text += response["choices"][0]["text"]
    except openai.error.OpenAIError as e:
        text += f"\nError: {str(e)}"
        
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)
    
    return text

#todo: add more app
dictapp = {"command prompt":"cmd","Word":"winword", "file explorer":"fileexp","media player":"wmplayer","task manager":"taskmgr","Excel":"excel","Firefox":"Firefox","spyder":"spyder","PowerPoint":"powerpnt"}
    
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
    Wishme()
    takeCommand()
    while True:
        if 1:
            query = takeCommand()#Converting user query into lower case
            #Logic for executing tasks based on query
            
            if "stop" in query or "bye" in query or "quit" in query:
                speak("Goodbye Sir, have a nice day!")
                break
            #todo: add more website
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
                speak(f"Playing {random_song}")
            
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
            
            elif "using artificial intelligence" in query:
                ai(prompt=query)
                speak("Doing sir")
                
            elif "Jarvis Quit".lower() in query.lower():
                exit()

            elif "reset chat".lower() in query.lower():
                chatStr = ""

            else:
                print("Chatting...")
                chat(query)
        
            
            
            
