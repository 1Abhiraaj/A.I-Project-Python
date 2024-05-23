import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import pywhatkit as wk
import webbrowser
import os
from dotenv import load_dotenv, dotenv_values
from News_website import webProject
from Environment_api import generation_config, genai
import pyautogui as pi
import time
from time import sleep
import random
import sys

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def say(text):
    os.system(f'say "{text}"')

def Wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis Sir. Please tell me how may I help you")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source)
        try:
            print("Recognizing....")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")
            return "None"
        return query

# Global variable to store chat history
# Initialize the chat string
chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    chatStr += f"Abhinav: {query}\nJarvis: "
    
    try:
        response = genai.generate_text(
            model="tunedModels/gemini-1.5-pro-latest",
            prompt=chatStr,
            temperature=generation_config["temperature"],
            max_output_tokens=generation_config["max_output_tokens"],
            top_p=generation_config["top_p"],
            top_k=generation_config["top_k"]
        )
        
        # Access the text generated by the model
        response_text = response['candidates'][0]['output']
        
        # This function is assumed to convert text to speech
        say(response_text)
        
        chatStr += f"{response_text}\n"
        return response_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

def ai(prompt):
    text = f"Generative AI response for Prompt: {prompt} \n *************************\n\n"
    
    try:
        response = genai.generate_text(
            model="tunedModels/gemini-1.5-pro-latest",
            prompt=prompt,
            temperature=generation_config["temperature"],
            max_output_tokens=generation_config["max_output_tokens"],
            top_p=generation_config["top_p"],
            top_k=generation_config["top_k"]
        )
        
        # Append the generated response to the text
        text += response['candidates'][0]['output']
        
        # Check if the "Openai" directory exists, and create it if it doesn't
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        
        # Generate a file name from the prompt and save the response text to the file
        with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
            f.write(text)
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    query = "Tell me a joke about artificial intelligence."
    ai(query)

# Example usage
if __name__ == "__main__":
    query = "Tell me a joke about artificial intelligence."
    ai(query)
    
dictapp = {"command prompt":"cmd","Word":"winword", "file explorer":"fileexp","media player":"wmplayer","task manager":"taskmgr","Excel":"excel","PowerPoint":"powerpnt"}

def openappweb(query):
    if ".com" in query or ".co.in" in query or ".org" in query:
        query = query.replace("open", "").replace("jarvis", "").replace("launch", "").replace(" ", "")
        webbrowser.open(f"https://www.{query}")
        speak("Launching, sir")
    else:
        for app in dictapp:
            if app in query:
                try:
                    os.system(f"start {dictapp[app]}")
                    speak(f"{app} opened")
                except Exception as e:
                    speak(f"Sorry, I couldn't open {app}")

def closeappweb(query):
    speak("Closing, sir")
    tab_count = 1
    if "one tab" in query or "1 tab" in query:
        tab_count = 1
    elif "2 tab" in query:
        tab_count = 2
    elif "3 tab" in query:
        tab_count = 3
    elif "4 tab" in query:
        tab_count = 4
    elif "5 tab" in query:
        tab_count = 5
    
    for _ in range(tab_count):
        pi.hotkey("ctrl", "w")
        sleep(0.5)
    
    for app in dictapp:
        if app in query:
            try:
                os.system(f"taskkill /f /im {dictapp[app]}.exe")
                speak(f"{app} closed")
            except Exception as e:
                speak(f"Sorry, I couldn't close {app}")

if __name__ == "__main__":
    print('Welcome to Jarvis A.I')
    Wishme()
    takeCommand()
    while True:
        query = takeCommand().lower()
        
        sites = [
            ["open youtube", "https://www.youtube.com"],
            ["open github", "https://www.github.com"],
            ["open google", "https://www.google.com"],
            ["open online gdb", "https://www.onlinegdb.com"]
        ]
        
        for site in sites:
            if f"open {site[0]}" in query:
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                speak("Opening Sir")
        
        if 'wikipedia' in query:
            speak('Searching from Wikipedia....')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=5)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        
        elif 'google search' in query:
            speak("What should I search?")
            qry = takeCommand().lower()
            url = f"https://www.google.com/search?q={qry}"
            speak(f"Searching Google for {qry}")
            webbrowser.open(url)
        
        elif 'youtube search' in query:
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
        
        elif "open web project" in query:
            webProject(query)
        
        elif 'play music' in query:
            music_dir = 'F:\\SONG\\A FOLDER'
            songs = os.listdir(music_dir)
            random_song = random.choice(songs)
            os.startfile(os.path.join(music_dir, random_song))
            speak(f"Playing {random_song}")
        
        elif 'volume up' in query:
            for _ in range(15):
                pi.press("volumeup")
        
        elif 'volume down' in query:
            for _ in range(15):
                pi.press("volumedown")
        
        elif "mute" in query or "unmute" in query:
            pi.press("volumemute")
        
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        
        elif "go to sleep" in query:
            try:
                speak('All right sir, I am switching off')
                sys.exit()
            except Exception as e:
                speak("Sorry, I couldn't go to sleep.")
        
        elif "take a screenshot" in query:
            pi.hotkey("win", "prtsc")
            speak('Tell me a name for the file')
            name = takeCommand().lower()
            sleep(3)
            img = pi.screenshot()
            img.save(f"{name}.png")
            speak("Screenshot saved")
        
        elif 'open camera' in query:
            try:
                os.system("start microsoft.windows.camera:")
                speak("Opening camera")
            except Exception as e:
                speak("Sorry, I couldn't open the camera.")
        
        elif "using artificial intelligence" in query:
            ai(prompt=query)
            speak("Doing sir")
        
        # elif "jarvis quit" in query:
        #     exit()
        
        # elif "reset chat" in query:
        #     chatStr = ""
        
        # else:
        #     chat(query)
