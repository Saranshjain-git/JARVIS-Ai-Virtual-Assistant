import platform
import os
import webbrowser
import datetime

import pywhatkit
import pyautogui
import speech_recognition as sr
import pyttsx3
import spacy
import screen_brightness_control as sbc
import subprocess
import psutil
import cv2

from transformers import pipeline
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_OPENAI_API_KEY"
)

# =========================
# NLP
# =========================

nlp = spacy.load("en_core_web_sm")

intent_classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# =========================
# SPEAK
# =========================

engine = pyttsx3.init()

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")

if voices:
    engine.setProperty("voice", voices[0].id)

def speak(text):

    print(f"\nJarvis: {text}")

    try:

        engine.stop()

        engine.say(text)

        engine.runAndWait()

    except Exception as e:

        print("Speech Error:", e)

 # =========================
# SAY HELPER
# =========================

def say(message):

    speak(message)

    return message

# =========================
# AI CHAT FUNCTION
# =========================

def ask_ai(question):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content

# =========================
# LISTEN
# =========================

recognizer = sr.Recognizer()

def listen_once():

    try:

        with sr.Microphone(device_index=1) as source:

            print("\nListening...")

            recognizer.energy_threshold = 300
            recognizer.pause_threshold = 1

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=15,
                phrase_time_limit=8
            )

            print("Recognizing...")

            text = recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            print("You said:", text)

            return text.lower()

    except sr.WaitTimeoutError:

        print("Listening timeout")

        return None

    except sr.UnknownValueError:

        print("Could not understand audio")

        return None

    except Exception as e:

        print("Microphone Error:", e)

        return None

# =========================
# HANDLE COMMAND
# =========================

def handle_command(text: str):

     print(
        "\nHANDLE COMMAND HIT:",
        text
    )

     t = text.lower().replace("-", " ").strip()

     t = t.replace(".", "")
     t = t.replace(",", "")
     t = t.replace("?", "")
     t = t.replace("!", "")

     print("CLEANED COMMAND =", t)

    # =========================
    # EXIT
    # =========================

     if any(w in t for w in [
        "exit",
        "quit",
        "bye",
        "stop jarvis"
    ]):

        speak("Goodbye Saransh")

        return "exit"

    # =========================
    # OPEN APPS / WEBSITES
    # =========================

        if t.startswith("open ") and not t.startswith("open file"):

         app = t.replace("open ", "").strip()

        apps = {

            "chrome": "start chrome",
            "google chrome": "start chrome",
            "notepad": "notepad",
            "calculator": "calc",
            "paint": "mspaint",
            "camera": "start microsoft.windows.camera:",
            "cmd": "start cmd",
            "powershell": "start powershell",
            "task manager": "taskmgr",
            "control panel": "control",
            "settings": "start ms-settings:",
            "whatsapp": "start whatsapp",
            "spotify": "start spotify",
            "telegram": "start telegram",
            "discord": "start discord",
            "explorer": "explorer",
            "file explorer": "explorer",
            "vs code": "code",
            "visual studio code": "code"
        }

        websites = {

            "youtube": "https://youtube.com",
            "google": "https://google.com",
            "instagram": "https://instagram.com",
            "facebook": "https://facebook.com",
            "github": "https://github.com",
            "linkedin": "https://linkedin.com",
            "chatgpt": "https://chat.openai.com",
            "amazon": "https://amazon.in",
            "netflix": "https://netflix.com"
        }

        if app in apps:

            os.system(apps[app])

            speak(f"Opening {app}")

            return

        if app in websites:

            webbrowser.open(websites[app])

            speak(f"Opening {app}")

            return

        speak(f"Searching {app}")

        pywhatkit.search(app)

        return
    # =========================
    # YOUTUBE
    # =========================

     if any(w in t for w in [

        "play",
        "song",
        "music",
        "video"
]):

        query = t

        remove_words = [
            "play",
            "youtube",
            "song",
            "music",
            "video",
            "on youtube",
            "chala",
            "chalao"
        ]

        for word in remove_words:
            query = query.replace(word, "")

        query = query.strip()

        if query:

            speak(f"Playing {query}")

            pywhatkit.playonyt(query)

        else:

            webbrowser.open("https://youtube.com")

            speak("Opening YouTube")

        return

    # =========================
    # GOOGLE SEARCH
    # =========================

     if any(w in t for w in [
        "search",
        "google",
        "find"
    ]):

        query = t

        remove_words = [
            "search",
            "google",
            "find"
        ]

        for word in remove_words:
            query = query.replace(word, "")

        query = query.strip()

        if query:

            speak(f"Searching {query}")

            pywhatkit.search(query)

        return

    

    # =========================
    # VOLUME
    # =========================

     if any(x in t for x in [
        "volume up",
        "increase volume",
        "awaz badhao",
        "sound up"
    ]):

        for _ in range(10):
            pyautogui.press("volumeup")

        speak("volume increased")

        return

     if any(x in t for x in [
        "volume down",
        "decrease volume",
        "awaz kam",
        "sound down"
    ]):

        for _ in range(10):
            pyautogui.press("volumedown")

        speak("Volume decreased")

        return

     if "mute" in t:

        pyautogui.press("volumemute")

        speak("Muted")

        return

    # =========================
    # BRIGHTNESS
    # =========================

     if any(x in t for x in [
        "brightness up",
        "increase brightness",
        "brightness badhao"
    ]):

        current = sbc.get_brightness()[0]

        sbc.set_brightness(
            min(current + 20, 100)
        )

        speak("Brightness increased")

        return

     if any(x in t for x in [
        "brightness down",
        "decrease brightness",
        "brightness kam"
    ]):

        current = sbc.get_brightness()[0]

        sbc.set_brightness(
            max(current - 20, 0)
        )

        speak("Brightness decreased")

        return

    # =========================
    # WIFI
    # =========================

     if any(x in t for x in [
        "wifi off",
        "turn off wifi",
        "turn off wi-fi",
        "wi-fi off"
    ]):

        os.system(
            'netsh interface set interface name="Wi-Fi" admin=disabled'
        )

        speak("WiFi turned off")

        return

     if any(x in t for x in [
        "wifi on",
        "turn on wifi",
        "turn on wi-fi",
        "wi-fi on"
    ]):

        os.system(
            'netsh interface set interface name="Wi-Fi" admin=enabled'
        )

        speak("WiFi turned on")

        return
     # =========================
    # BLUETOOTH OFF
    # =========================

     if any(x in t for x in [
        "bluetooth off",
        "turn off bluetooth"
    ]):

        print("BLUETOOTH OFF HIT")

        speak("Turning Bluetooth off")

        result = subprocess.run(
            [
                "powershell",
                "-Command",
                "Disable-PnpDevice -InstanceId 'USB\\VID_8087&PID_0029\\6&3BD0080&0&4' -Confirm:$false"
            ],
            capture_output=True,
            text=True
        )

        print(result.stdout)
        print(result.stderr)

        speak("Bluetooth turned off")

        return
     # =========================
    # BLUETOOTH ON
    # =========================

     if any(x in t for x in [
        "bluetooth on",
        "turn on bluetooth"
    ]):

        print("BLUETOOTH ON HIT")

        speak("Turning Bluetooth on")

        result = subprocess.run(
            [
                "powershell",
                "-Command",
                "Enable-PnpDevice -InstanceId 'USB\\VID_8087&PID_0029\\6&3BD0080&0&4' -Confirm:$false"
            ],
            capture_output=True,
            text=True
        )

        print(result.stdout)
        print(result.stderr)

        speak("Bluetooth turned on")

        return
    # =========================
    # SCREENSHOT
    # =========================
     if any(x in text.lower() for x in [
        "screenshot",
        "take screenshot",
        "capture screen"
    ]):

        ...
        

    # =========================
    # SCREENSHOT
    # =========================

        if any(x in text.lower() for x in [
        "screenshot",
        "take screenshot",
        "capture screen"
    ]):

         path = os.path.join(
            os.getcwd(),
            "screenshot.png"
        )

        screenshot = pyautogui.screenshot()
        screenshot.save(path)

        return say("Screenshot saved")
    # =========================
    # LOCK PC
    # =========================

     if any(x in t for x in [
        "lock pc",
        "lock computer"
    ]):

        speak("Locking computer")

        os.system(
            "rundll32.exe user32.dll,LockWorkStation"
        )

        return

    # =========================
    # SHUTDOWN
    # =========================

     if any(x in t for x in [
        "shutdown",
        "shut down"
    ]):

        speak("Shutting down computer")

        os.system(
            "shutdown /s /t 5"
        )

        return

    # =========================
    # RESTART
    # =========================

     if any(x in t for x in [
        "restart",
        "reboot"
    ]):

        speak("Restarting computer")

        os.system(
            "shutdown /r /t 5"
        )

        return

    # =========================
    # SLEEP
    # =========================

     if any(x in t for x in [
        "sleep pc",
        "sleep computer"
    ]):

        speak("Putting computer to sleep")

        os.system(
            "rundll32.exe powrprof.dll,SetSuspendState Sleep"
        )

        return

   
   

    # =========================
    # CREATE FOLDER
    # =========================

     if "create folder" in t:

        name = t.replace(
            "create folder",
            ""
        ).strip()

        if name:

            path = os.path.join(
                os.getcwd(),
                name
            )

            os.makedirs(path, exist_ok=True)

            speak(f"Folder {name} created")

        return


    # =========================
    # OPEN FILE
    # =========================

     if t.startswith("open file"):

        print("OPEN FILE BLOCK EXECUTED")

        file_name = t.replace(
            "open file",
            ""
        ).strip().lower()

        speak(f"Searching file {file_name}")

        folders = [
            os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop"),
            os.path.join(os.path.expanduser("~"), "Desktop"),
            os.path.join(os.path.expanduser("~"), "Downloads"),
            os.path.join(os.path.expanduser("~"), "Documents")
        ]

        found = False

        for folder in folders:

            if not os.path.exists(folder):
                continue

            for root, dirs, files in os.walk(folder):

                for file in files:

                    if any(
                        word in file.lower()
                        for word in file_name.split()
                    ):

                        full_path = os.path.join(root, file)

                        print("FOUND:", full_path)

                        os.startfile(full_path)

                        speak(f"Opening {file}")

                        found = True

                        break

                if found:
                    break

            if found:
                break

        if not found:
            speak("File not found")

        return

        
      # =========================
    # SYSTEM INFO
    # =========================

     if "system info" in t:

        speak(
            f"You are using {platform.system()} {platform.release()}"
        )

        return
    # =========================
    # BATTERY
    # =========================

     if any(x in t for x in [
        "battery",
        "battery percentage",
        "battery status"
    ]):

        battery = psutil.sensors_battery()

        if battery:

            percent = battery.percent

            speak(f"Battery is {percent} percent")

        else:

            speak("Battery information not available")

        return
    # =========================
    # CAMERA PHOTO
    # =========================

     if any(x in t for x in [
        "take photo",
        "capture photo",
        "camera photo"
    ]):

        cam = cv2.VideoCapture(0)

        ret, frame = cam.read()

        if ret:

            path = os.path.join(
                os.getcwd(),
                "photo.jpg"
            )

            cv2.imwrite(
                path,
                frame
            )

            speak("Photo captured")

        else:

            speak("Unable to access camera")

        cam.release()

        return

    # =========================
    # JARVIS STATUS
    # =========================

     if any(x in t for x in [
        "jarvis status",
        "status",
        "are you online"
    ]):

        battery = psutil.sensors_battery()

        battery_percent = battery.percent if battery else "unknown"

        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent(interval=1)

        speak(
            f"I am online. Battery {battery_percent} percent. RAM usage {ram} percent. CPU usage {cpu} percent."
        )

        return

       
    
    # =========================
    # FALLBACK
    # =========================

     speak("Searching on Google")
     pywhatkit.search(t)

# =========================
# MAIN
# =========================

def main():

    speak("Hello Saransh. Jarvis is online.")

    while True:

        text = listen_once()

        if not text:
            continue

        result = handle_command(text)

        if result == "exit":
            break

# =========================
# START
# =========================

if __name__ == "__main__":
    main()