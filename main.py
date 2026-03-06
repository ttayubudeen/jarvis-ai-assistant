import speech_recognition as sr
import webbrowser
import pyautogui
from datetime import datetime
import requests
import subprocess
import uuid
from pydub import AudioSegment
from openai import OpenAI
from gtts import gTTS
import pygame
import os
from config import openai_api_key
from config import google_api_key
from config import news_api_key

# requirement , ask for what to put in requirement.txt



# backup TTS
def speak_old(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

pygame.mixer.init()

# speak function, TTS func
def speak(text):
    try:
        filename = f"voice_{uuid.uuid4().hex}.wav"

        subprocess.run(
            ["piper", "--model", "voices/en_GB-alan-medium.onnx", "--output_file", filename],
            input=text,
            text=True
        )

        # speed up audio slightly
        sound = AudioSegment.from_file(filename)
        sound = AudioSegment.silent(duration=100) + sound
        faster = sound.speedup(playback_speed=1.1)   # adjust speed here
        faster.export(filename, format="wav")

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        os.remove(filename)
    except Exception as e:
        print("ATTENTION : THE SPEAK FUNCTION IS GONE !!!")
        print("ERROR in SPEAK :",e)

# AI reply func
def aiProcess(command):
    try:
        client = OpenAI(api_key=openai_api_key,
        )

        completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are J.A.R.V.I.S., a calm, polite, witty AI assistant. Give a single, short, helpful, and intelligent response. Do not ask questions or offer to continue. Act exactly like J.A.R.V.I.S. would."},
            {"role": "user", "content": command}
        ]
        )

        return completion.choices[0].message.content

    except Exception as e:
        speak("  That information is not available to me at the moment, sir. Perhaps I can assist you with something else")
        print("ERROR in Openai API :",e)


# media func
def get_youtube_link(query):
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": 1,
            "key": google_api_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        # print(data)
        
        if "items" in data and len(data["items"]) > 0:
            video_id = data["items"][0]["id"]["videoId"]
            return f"https://www.youtube.com/watch?v={video_id}"
        else:
            return None
    except Exception as e:
        speak("  That media source appears temporarily unavailable, Sir. Shall we try something else?")
        print("ERROR in youtube API :", e)

# news func
def current_news():
    try:
        url = "https://newsdata.io/api/1/latest"

        params = {
            "apikey": news_api_key,
            "country": "in,us,cn,ca,ru",
            "language": "en",
            "category": "technology,science,crime"
        }

        response = requests.get(url, params=params)
        data = response.json()

        # Extract unique headlines and limit to 5
        seen = set()
        headlines = []
        for item in data.get("results", []):
            title = item.get("title")
            if title and title not in seen:
                seen.add(title)
                headlines.append(title)
            if len(headlines) >= 5:
                break

        # Store in a single variable
        top_headlines = headlines  # This is now a list variable containing the top 5 headlines

        # Add numbered prefix to each headline
        news_list_numbered = [f"headline {i+1} , {headline}" for i, headline in enumerate(top_headlines)]

        # Convert to a single string if needed
        news_str = ", ".join(news_list_numbered)

        print("Jarvis : The top headlines, Sir.")
        speak("The top headlines, Sir.")
        print("Jarvis :",news_str)
        speak(news_str)

    except Exception as e:
        speak("I'm unable to access that category at the moment, Sir. How else may I assist you?")
        print("ERROR in news API :", e)

# website dictionary
sites = {
            "google": "https://google.com",
            "youtube": "https://youtube.com",
            "github": "https://github.com",
            "linkedin": "https://linkedin.com",
            "wikipedia": "https://wikipedia.org",
            "gmail": "https://mail.google.com"
        }



def processCommand(c):
    try:
        command = c.lower().strip()

        # check is user is repeating Jarvis
        if command == "jarvis":
            print("Jarvis : I'm here, Sir.")
            speak("I'm here, Sir.")


        elif "open" in command:
            for site, url in sites.items():
                if site in command:
                    response = f"Opening {site}, sir."
                    print("Jarvis:", response)
                    speak(response)
                    webbrowser.open(url)
                    return

        elif "play news" in command or "play the news" in command:
            current_news()

        
        elif "screenshot" in command:
            response = "I've taken the screenshot, Sir. Resolution is set to full display parameters."

            img = pyautogui.screenshot()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            img.save(filename)
            
            print("Jarvis :", response)
            speak(response)
        
        elif "play" in command:
            # Example usage
            song_name = c.lower().replace("play", "").strip()
            raw_link = get_youtube_link(song_name)
            link = raw_link
            webbrowser.open(link)
            print("Jarvis : Certainly, sir.")
            speak(" ,Certainly, sir.")
            # print("YouTube Link:", link)

        else:
            # Let OpenAI handle the request
            output = aiProcess(c)
            print("Jarvis :",output)
            speak(output)

    except Exception as e:
        print("ERROR in Command Process , Need Attention in the Command Process !!!")
        print("ERROR in Command Process :", e)
   

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    print("Initializing Jarvis....")

    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone

         

        try:
            with sr.Microphone() as source:
                print("\nJarvis Listening...")
                audio = r.listen(source, timeout=3, phrase_time_limit=1.1)
            word = r.recognize_google(audio)
            wake_word = word.lower().replace(" ", "").strip()
            if "jarvis" in wake_word:
                speak(" ,Yes sir?")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    r.dynamic_energy_threshold = True
                    r.adjust_for_ambient_noise(source, duration=0.6)
                    r.pause_threshold = 1.5
                    audio = r.listen(source, timeout=5, phrase_time_limit=15)
                    command = r.recognize_google(audio)
                    # print(command)
                    print("\nUser :",command)
                    processCommand(command)

        except sr.WaitTimeoutError:
            pass  # ignore normal timeout

        except Exception as e:
            print("Unclear Input; {0}".format(e))