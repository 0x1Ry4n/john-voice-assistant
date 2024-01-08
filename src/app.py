import chatbot
import pyttsx3
import speech_recognition as sr
import pynput.keyboard as k
import time
import sys
from controllers.gesture import GestureController
from controllers.clipboard import ClipBoard
from controllers.files import FileHandler
from controllers.localtime import LocalTime
from controllers.web_search import *
from threading import Thread


class Bot:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.8
        self.recognizer.energy_threshold = 300
        self.engine = pyttsx3.init("sapi5")
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", self.voices[2].id)
        self.keyboard = ClipBoard(keyboard=k.Controller())
        self.is_awake = True
        self.enable_weather_answer = True

    def record_audio(self):
        with sr.Microphone() as source:
            voice_data = ""
            audio = self.recognizer.listen(source, phrase_time_limit=8)

            try:
                voice_data = self.recognizer.recognize_google(audio)
            except sr.RequestError:
                self.reply(
                    "Sorry, my Service is down. Please, check your Internet connection"
                )
            except sr.UnknownValueError:
                print("Could not understand the voice")
            except Exception as e:
                print(e)

            return voice_data.lower()

    def reply(self, audio):
        chatbot.ChatBot.addAppMsg(audio)
        self.engine.say(audio)
        self.engine.runAndWait()

    def all_commands(self, static_commands):
        commands = [key for key in static_commands.keys()]
        list_of_commands = ""

        for c in commands:
            list_of_commands += "- " + c + "<br>"

        self.reply("These are the list of commands")
        chatbot.ChatBot.addAppMsg(list_of_commands)

    def wish(self):
        try:
            actual_hour = LocalTime.hour()
            actual_location = Location()
            actual_location = actual_location.search_location_by_ip()

            if 0 <= actual_hour < 12:
                self.reply("Good Morning!")
            elif 12 <= actual_hour < 18:
                self.reply("Good Afternoon!")
            else:
                self.reply("Good Evening!")

            if actual_location is None:
                self.reply("Cannot determine your actual location!")

            self.reply(
                f"You are in {actual_location['city']} - {actual_location['regionName']} - {actual_location['country']} "
            )
            self.enable_weather_answer = False

            self.weather(actual_location["city"])
            self.enable_weather_answer = True
        except Exception as e:
            print(e)

    def weather(self, city=None):
        try:
            weather_controller = Weather()

            audio = city

            if self.enable_weather_answer:
                self.reply("Which place weather are you looking for?")
                audio = self.record_audio()
                chatbot.ChatBot.addUserMsg(audio)

            if self.enable_weather_answer:
                self.reply("Collecting...")

            actual_weather = weather_controller.search_weather(audio)

            if actual_weather is None:
                self.reply("City not found!")

            self.reply(
                f'Actual temperature is {actual_weather["temperature"]} celsius degrees'
            )
            self.reply(f'Actual humidity is {actual_weather["humidity"]} per cent')
            self.reply(
                f'Currently, the city is experiencing {actual_weather["description"]}'
            )
        except Exception as e:
            print(e)

    def location(self):
        try:
            self.reply("Which place are you looking for ?")
            voice_data = self.record_audio()
            chatbot.ChatBot.addUserMsg(voice_data)
            self.reply("Locating...")

            location = Location.search_by_google_maps(voice_data)

            if location is None:
                self.reply("Location not found!")

            self.reply("This is what I found Sir")
        except Exception as e:
            raise e

    def list_files(self):
        file_controller = FileHandler()
        objects = file_controller.list_files()

        if objects is None:
            self.reply("Any file founded!")

        self.reply("These are the files in your root directory")
        chatbot.ChatBot.addAppMsg(objects)

    def open_file(self, voice_data):
        file_controller = FileHandler()
        file = file_controller.open_file(voice_data)

        if file is None:
            self.reply("File not found!")

        if file == -1:
            self.reply("You do not have permission to access this folder!")

        self.reply("Opened Successfully!")
        chatbot.ChatBot.addAppMsg(file)

    def back(self):
        file_controller = FileHandler()
        file = file_controller.back()

        self.reply("Ok")
        chatbot.ChatBot.addAppMsg(file)

    def launch_gesture_recognition(self):
        if GestureController.gc_mode:
            self.reply("Gesture recognition is already active")
        else:
            gc = GestureController()
            thread = Thread(target=gc.start)
            thread.start()
            self.reply("Launched Successfully")

    def stop_gesture_recognition(self):
        if GestureController.gc_mode:
            GestureController.gc_mode = 0
            self.reply("Gesture recognition stopped")
        else:
            self.reply("Gesture recognition is already inactive")

    def search(self, voice_data):
        try:
            voice_data = " ".join(voice_data)

            self.reply("Searching for " + voice_data)

            content = Search.search_by_google(voice_data)

            if content is None:
                self.reply("Content not found!")

            self.reply("This is what I found Sir")
        except Exception as e:
            print(e)

    def download_video_from_youtube(self, voice_data, only_audio=True):
        try:
            voice_data = " ".join(voice_data)

            self.reply(f"Searching for video {voice_data}")

            time_consumed = Search.download_youtube_video(
                voice_data, only_audio=only_audio
            )

            if time_consumed is None:
                self.reply("Video not found!")

            self.reply(f"Video downloaded in {str(time_consumed)} seconds")
        except Exception as e:
            print(e)

    def copy(self):
        self.keyboard.copy()
        self.reply("Copied")

    def paste(self):
        self.keyboard.paste()
        self.reply("Pasted")

    def exit(self):
        if GestureController.gc_mode:
            GestureController.gc_mode = 0
        chatbot.ChatBot.close()
        sys.exit()

    def bye(self):
        self.reply("Good bye Sir! Have a nice day.")
        self.is_awake = False

    def handle_commands(self, voice_data, bot_commands):
        command_parts = voice_data.split(" ", 1)
        extra_data = command_parts[1].strip() if len(command_parts) > 1 else None

        if extra_data is None:
            return None

        param = extra_data.split()
        args = param[1:]

        if param[0] in ["open", "search", "download"]:
            if param[0] == "download":
                args = param[3:]
                param = " ".join(param[0:3])
                bot_commands[param](args)
            else:
                bot_commands[param[0]](args)
        elif param[0] in ["commands"]:
            bot_commands[param[0]]()
        elif extra_data in bot_commands:
            bot_commands[extra_data]()
        else:
            bot_commands["error"]()

    def respond(self, voice_data):
        try:
            chatbot.ChatBot.addUserMsg(voice_data)

            if self.is_awake is False:
                if "wake up" in voice_data:
                    self.is_awake = True
                    self.wish()

            bot_commands = {
                "what's your name": lambda: self.reply("My name is John!"),
                "commands": lambda: self.all_commands(bot_commands),
                "date": lambda: self.reply(LocalTime.date()),
                "time": lambda: self.reply(LocalTime.time()),
                "error": lambda: self.reply(
                    "I'm sorry, the command you entered does not exist"
                ),
                "search": lambda voice_data: self.search(voice_data),
                "download youtube audio": lambda voice_data: self.download_video_from_youtube(
                    voice_data
                ),
                "download youtube video": lambda voice_data: self.download_video_from_youtube(
                    voice_data, only_audio=False
                ),
                "open file": lambda voice_data: self.open_file(voice_data),
                "list files": self.list_files,
                "back": self.back,
                "hello": self.wish,
                "launch gesture recognition": self.launch_gesture_recognition,
                "stop gesture recognition": self.stop_gesture_recognition,
                "location": self.location,
                "weather": self.weather,
                "copy": self.copy,
                "paste": self.paste,
                "bye": self.bye,
                "exit": self.exit,
            }

            self.handle_commands(voice_data, bot_commands)
        except Exception as e:
            print(e)


def main():
    try:
        bot = Bot()

        t1 = Thread(target=chatbot.ChatBot.start)
        t1.start()

        while not chatbot.ChatBot.started:
            time.sleep(0.5)

        bot.wish()

        voice_data = None

        while True:
            if chatbot.ChatBot.isUserInput():
                voice_data = chatbot.ChatBot.popUserInput()
            else:
                voice_data = bot.record_audio()

            if "john" in voice_data:
                try:
                    bot.respond(voice_data)
                except SystemExit:
                    bot.reply("Exit Successful")
                except Exception as e:
                    print(f"Exception raised while responding: {e}")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
