import speech_recognition as sr

r = sr.Recognizer()

mic = sr.Microphone(device_index=1)

with mic as source:
    print("BOL ABHI...")
    r.adjust_for_ambient_noise(source, duration=2)
    audio = r.listen(source, timeout=20)

print("RECOGNIZING...")

try:
    text = r.recognize_google(audio, language="en-IN")
    print("YOU SAID:", text)

except Exception as e:
    print("ERROR:", e)
