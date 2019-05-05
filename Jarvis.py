# -*- coding: utf-8 -*-
from gtts import gTTS   # Text to speech
import locale
import time

# Parsing strings with tagger
from nltk.tag import StanfordPOSTagger
import os

# Const
TOP_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL = TOP_DIR + '/resources/standford_tagger/models/french.tagger'
JAR_FILE = TOP_DIR + '/resources/standford_tagger/stanford-postagger.jar'

# init stanford tagger
st = StanfordPOSTagger(MODEL, JAR_FILE)


class Jarvis:
    def __init__(self):
        locale.setlocale(locale.LC_TIME, '')

    @staticmethod
    def speak(text_to_speech):
        print("jarvis :" + text_to_speech)
        tts = gTTS(text_to_speech, 'fr')
        tts.save("audio.mp3")
        os.system("mpg123 audio.mp3")
        os.remove("audio.mp3")

    def think(self, audiosource):
        if "comment ça va" in audiosource:
            self.speak("ça va bien.")
        elif "ça va" in audiosource:
            self.speak("ça va bien.")

        if "quelle heure est-il" in audiosource:
            self.speak('il est ' + time.strftime('%-H') + ' heure ' + time.strftime('%M'))
        elif "quelle heure il est" in audiosource:
            self.speak('il est ' + time.strftime('%-H') + ' heure ' + time.strftime('%M'))