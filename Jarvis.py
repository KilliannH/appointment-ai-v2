# -*- coding: utf-8 -*-
from gtts import gTTS   # Text to speech
import locale
import datetime
import time
import json

# Parsing strings with tagger
from nltk.tag import StanfordPOSTagger
import os

# Const
TOP_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL = TOP_DIR + '/resources/standford_tagger/models/french.tagger'
JAR_FILE = TOP_DIR + '/resources/standford_tagger/stanford-postagger.jar'

# init stanford tagger
st = StanfordPOSTagger(MODEL, JAR_FILE)

date_advs = ["aujourd'hui", "demain", "après-demain"]
weekDays_fr = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
months_fr = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "décembre"]
dateKeywords_fr = ["prochain", "semaine", "mois", "jour", "hier"]


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

class Jarvis:

    user = {'wantsAction': False, 'action': '', 'appointment': False, 'appointmentName': '', 'date': datetime.date.today()}

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
        output = st.tag(audiosource.split())

        #  CREATE  ##

        if output[0][1] == 'VINF':
            # we know the user wants an action here
            self.user['wantsAction'] = True
            if output[0][0] == 'créer':
                self.user['action'] = 'CREATE'

        if self.user['wantsAction'] and self.user['action'] == 'CREATE':
            for i in range(0, len(output)):
                if output[i][1] == 'NC':
                    if output[i][0] == 'rendez-vous':
                        # we know the user wants to create an appointment
                        self.user['appointment'] = True
                        break

        if self.user['appointment']:
            print(output)
            appointment_name_arr = []
            appointment_name = ''
            for i in range(0, len(output)):
                if output[i][1] == 'NC':
                    if output[i][0] != 'rendez-vous':
                        # we guess the name of the appointment
                        appointment_name_arr.append(output[i][0])
                elif output[i][1] == 'ADJ':
                    appointment_name_arr.append(output[i][0])

            # sort the name in some way
            sort = []
            for i in range(0, len(appointment_name_arr)):
                for j in range(0, len(dateKeywords_fr)):
                    if appointment_name_arr[i] in dateKeywords_fr[j]:
                        sort.append(appointment_name_arr[i])

                for j in range(0, len(date_advs)):
                    if appointment_name_arr[i] in date_advs[j]:
                        sort.append(appointment_name_arr[i])

                for j in range(0, len(weekDays_fr)):
                    if appointment_name_arr[i] in weekDays_fr[j]:
                        sort.append(appointment_name_arr[i])

            for i in range(0, len(sort)):
                appointment_name_arr.remove(sort[i])

            for i in range(0, len(appointment_name_arr)):
                if i < len(appointment_name_arr) - 1:
                    appointment_name += appointment_name_arr[i] + ' '
                else:
                    appointment_name += appointment_name_arr[i]

            self.user['appointmentName'] = appointment_name

        appointment_date = 0

        if self.user['appointment']:
            for i in range(0, len(output)):
                if output[i][1] == 'ADV':
                    # we guess the user wants a date by an adverb
                    for j in range(0, len(date_advs)):
                        if output[i][0] == date_advs[j]:

                            # we guess the adverb used for the date
                            appointment_date = datetime.date.today()

                            if j == 0:  # today
                                pass
                            elif j == 1:  # tomorrow
                                appointment_date += datetime.timedelta(days=1)
                            elif j == 2:  # in 2 days
                                appointment_date += datetime.timedelta(days=2)

            self.user['date'] = appointment_date

        dayfound = 0
        monthfound = 0
        yearfound = 0

        if appointment_date == 0:
            # that means date is not in date_advs array

            # find if there is a day in request
            for i in range(0, len(output)):
                for j in range(0, len(weekDays_fr)):
                    if output[i][0] == weekDays_fr[j]:
                        dayfound = weekDays_fr[j]
                        break

            # find if there is a month in request
            for i in range(0, len(output)):
                for j in range(0, len(months_fr)):
                    if output[i][0] == months_fr[j]:
                        monthfound = months_fr[j]
                        break

        if dayfound != 0 and monthfound == 0:
            # we might be in a case like "mardi prochain, mercredi prochain"

            # ensure we are in 'prochain' case
            nextinrequest = False

            for i in range(0, len(output)):
                if output[i][0] == dateKeywords_fr[0]:
                    nextinrequest = True
                    break

            if nextinrequest:
                appointment_date = next_weekday(datetime.date.today(), weekDays_fr.index(dayfound))

            # ## have to check a "jeudi DANS deux semaines" case here
            # and year, we 're still in the dayfound != 0 and monthfound == 0: case


#### # after we'll check year, if year on query -> set year, else -> set nearest year


        self.user['date'] = appointment_date


        print(self.user)
        self.speak("J'ai créé un rendez-vous, " + self.user['appointmentName'] + " le " + str(self.user['date'].strftime('%A %d %B %Y')))


        if 'DET' in output[0][1] and 'heure' in output[1][0]:
            self.speak('il est ' + time.strftime('%-H') + ' heure ' + time.strftime('%M'))
