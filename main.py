# -*- coding: utf-8 -*-

import speech_recognition as sr  # Speech to text recognition
from Jarvis import Jarvis

jarvis = Jarvis()

fname = 'record.wav'


def audio_recorder_callback(fname):
    print("Snowdboy_engine : converting audio to text")
    r = sr.Recognizer()
    with sr.AudioFile(fname) as source:
        audio = r.record(source)  # read the entire audio file
    data = ""
    try:
        data = r.recognize_google(audio, language='fr-FR')
        print("You said: " + data)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        jarvis.speak("Je n'ai pas compris ce que tu as dit.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        jarvis.speak("Je n'ai pas réussi à requêter Google, essaie encore !")

    return jarvis.think(data)


audio_recorder_callback(fname)
