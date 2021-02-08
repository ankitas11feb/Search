import speech_recognition as sr
import urllib.request
from bs4 import BeautifulSoup
import pyttsx3
import pymysql as MySQLdb

sr.Microphone(device_index=1)
r = sr.Recognizer()
r.energy_threshold = 5000
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 150)

db = MySQLdb.connect(host="localhost", database="googledb", user="root", password="root")
cursor = db.cursor()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def engine_speak(text):
    text = str(text)
    engine.say(text)
    engine.runAndWait()


with sr.Microphone() as source:
    print("Say!")
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("You said : {}".format(text))
        str = text.split()
        str2 = ('\+'.join(str))

        # Perform the request
        request = urllib.request.Request('https://google.com/search?q=' + str2)
        # Set a normal User Agent header, otherwise Google will block the request.
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/87.0.4280.88 Safari/537.36')
        raw_response = urllib.request.urlopen(request).read()
        # Read the response as a utf-8 string
        html = raw_response.decode("utf-8")
        # The code to get the html contents here.
        soup = BeautifulSoup(html, 'html.parser')
        # Find all the search result divs
        divs = soup.select("#search div.g")
        for div in divs:
            # Search for a h3 tag
            results = div.select("h3")
            print(div.get_text() + "\n\n")
            speak(div.get_text())
            s = div.get_text()
            # Check if we have found a result
            if len(results) >= 1:
                # Print the title
                h3 = results[0]
                speak(h3)
                print(h3.get_text())
                p = h3.get_text()

                sql = "INSERT INTO des(title, description) VALUES(%s,%s)"
                val = (s, p)
                print(val)
                cursor.execute(sql, val)
                print('value is executed')
                sql2 = "SELECT `title`,`description` FROM `des`"
                cursor.execute(sql2)
                print(" sql2 is executed")
                db.commit()
                db.close()
    except:
        print("Couldn't recognize")
