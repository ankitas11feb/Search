import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
from datetime import date, time
import mysql.connector
from mysql.connector import Error


class User():
    # Connection with mysql database
    try:
        connection = mysql.connector.connect(host='localhost', database='ankita11', user='root', password='root')
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You are connected to database : ", record)
    except Error as e:
        print("Error while connecting to MySQL", e)

    def __init__(self, email=None, password=None):
        self.mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="ankita11")
        self.myCursor = self.mydb.cursor(buffered=True)

        def register(self):
            if email == None and password == None:
                print("==== Register ====")
                self.email = input("Enter Email: ")
                self.password = input("Enter Password: ")

                sql2 = "SELECT * FROM users WHERE `email` = '" + self.email + "'"
                self.myCursor.execute(sql2)
                results = self.myCursor.fetchall()

                if len(results) > 0:
                    print("User is already exist.....")
                    print("Please Login")
                else:
                    sql = "INSERT INTO `users` (`email`, `password`) VALUES ('" + self.email + "','" + self.password + "')"
                    self.myCursor.execute(sql)
                    self.mydb.commit()
                    print("Registration Successful !!!!!")
                    print("Please Login")
            else:
                print("Registration Failed !!!!!")
                exit()

        def login(self):
            global static_var
            global static_var1

            if email == None and password == None:
                print("==== Login ====")
                self.email = input("Enter Email: ")
                self.password = input("Enter Password: ")

                sql = "SELECT `email`,`password` FROM `users`"
                self.myCursor.execute(sql)
                for (mail, pswd) in self.myCursor:
                    if self.email == mail and self.password == pswd:

                        log = True
                        break
                    else:
                        log = False
                if log == True:
                    print("Login Successful !!!!!")
                    sql3 = "select userid from users where email = '" + self.email + "'"
                    self.myCursor.execute(sql3)
                    result = self.myCursor.fetchone()
                    for i in result:
                        print(i)
                    static_var1 = i
                    static_var = self.email


                else:
                    print("Incorrect Email or Password.....")
                    print("You want to register? y/n")
                    Answer = input()
                    if Answer == "y":
                        register(self)
                    elif Answer == "n":
                        login(self)
                    else:
                        exit()
            else:
                print("Login Failed !!!!!")
                exit()

        while True:
            print("You want to register? y/n")
            Answer = input()
            if Answer == "y":
                register(self)
                break
            elif Answer == "n":
                login(self)
                break
            else:
                print("Please enter valid input")

        print()
        print()
        print('Loading your AI personal assistant - Flixy ...')
        print("Please wait...")
        print()
        print()

        listener = sr.Recognizer()
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('rate', 150)
        engine.setProperty('voice', voices[1].id)
        wake = "shane"

        def speak(text):
            engine.say(text)
            engine.runAndWait()

        def engine_speak(text):
            text = str(text)
            engine.say(text)
            engine.runAndWait()

        def record_audio(ask=""):
            with sr.Microphone() as source:  # microphone as source
                if ask:
                    engine_speak(ask)
                voice = listener.listen(source, 5, 5)  # listen for the audio via source
                print("Done Listening")

        count = 0
        multi_answer = 5

        # wake up
        def sayCommand():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                speak("Please say something")
                r.pause_threshold = 1
                audio = r.listen(source)
                print("Recognizing...")
                asd = r.recognize_google(audio, language='en-in', show_all=True)
                print(asd)
                speak("I am ready")
                print("How may i help you...")

        jackhammer = sr.AudioFile("D:\jackhammer.wav")
        with jackhammer as source:
            voice = listener.listen(source)

        command = listener.recognize_google(voice)

        with jackhammer as source:
            listener.adjust_for_ambient_noise(source, duration=0.5)
            audio = listener.record(source)

        command = listener.recognize_google(voice)

        def take_command(self):
            try:
                with sr.Microphone() as source:
                    print('listening...')
                    voice = listener.listen(source)
                    command = listener.recognize_google(voice)
                    command = command.lower()
                    if 'flixy' in command:
                        command = command.replace('flixy', '')
                        print(command)

            except:
                pass
            return command

        # Known Command History
        def save(self, command):
            try:
                self.mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="ankita11")
                self.myCursor = self.mydb.cursor()
                binary = 0
                today = date.today()
                d = today.strftime("%Y-%m-%d")
                print("values are printed")
                print(static_var1)
                #    time = datetime.datetime.now().strftime('%H:%M:%S')
                #    sql = "INSERT INTO `history1` (`email`,`userid`, `command`, `known`, `unknown`, `date`) " \
                #      +"VALUES ('" + static_var + "','" + static_var1 + "','" + command + "','" + str(binary) + "','" + d + "')"
                sql = "INSERT INTO history1 (email,userid, command, known, date) VALUES (%s, %s,%s,%s,%s) "
                val = (static_var, static_var1, command, str(binary), d)
                #    val = ("as", "9", "Hello ", "0", "021-01-15")
                print(sql)
                self.myCursor.execute(sql, val)
                self.mydb.commit()
                print('command are saved by try')
            except:
                pass

        # Unknown Command History
        def notsave(self, command):
            try:
                self.mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="ankita11")
                self.myCursor = self.mydb.cursor()
                binary = 1
                today = date.today()
                d = today.strftime("%Y-%m-%d")
            #    time = datetime.datetime.now().strftime('%H:%M:%S')
                #    sql = "INSERT INTO `history1` (`email`,`userid`, `command`, `known`, `unknown`, `date`) " \
                #          "VALUES ('" + static_var + "','" + static_var1 + "','" + command + "'," + str(binary) + ",'" + d + "')"
                sql = "INSERT INTO history1 (email,userid, command,unknown, date)VALUES (%s,%s,%s,%s,%s)"
                val = (static_var, static_var1, command, str(binary), d)
                self.myCursor.execute(sql, val)
                self.mydb.commit()
            #    print('commands are unknown')
            except:
                pass

        # saving all commands
        def prompt(self, command):
            try:
                self.mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="ankita11")
                self.myCursor = self.mydb.cursor()
                today = date.today()
                d = today.strftime("%Y-%m-%d")
            #    time = datetime.datetime.now().strftime('%H:%M:%S')
                sql = "INSERT INTO  `commands` (`command`,`date`) VALUES ('" + command + "','" + d + "')"
                self.myCursor.execute(sql)
                self.mydb.commit()
            except:
                pass

        # Saving All Answers
        def ans(self, a):
            try:
                self.mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="ankita11")
                self.myCursor = self.mydb.cursor()
                today = date.today()
                d = today.strftime("%Y-%m-%d")
            #    time = datetime.datetime.now().strftime('%H:%M:%S')
                sql = "INSERT INTO  `answers` (`answer`,`date`) VALUES ('" + a + "','" + d + "')"
                self.myCursor.execute(sql)
                self.mydb.commit()
            except:
                pass

        def run_flixy(self):
            command = take_command(self)
            print(command)

            # Wikipedia
            if 'open google' in command:
                save(self, command)
                webbrowser.open_new_tab("https://www.google.com")
                a = "google chrome is open now"
                ans(self, a)
                print(a)
                speak(a)
            else:
                notsave(self, command)
                a = "i don't know, Please say the command again"
                ans(self, a)
                print(a)
                speak(a)

        sayCommand()
        while True:
            run_flixy(self)


u = User()
