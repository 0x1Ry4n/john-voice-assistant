import eel
import os
from config.settings import CHATBOT_HOST, CHATBOT_PORT
from queue import Queue


class ChatBot:
    started = False
    userinputQueue = Queue()

    def isUserInput():
        return not ChatBot.userinputQueue.empty()

    def popUserInput():
        return ChatBot.userinputQueue.get()

    def close_callback(route, websockets):
        exit()

    @eel.expose
    def getUserInput(msg):
        ChatBot.userinputQueue.put(msg)
        print(msg)

    def close():
        ChatBot.started = False

    def addUserMsg(msg):
        eel.addUserMsg(msg)

    def addAppMsg(msg):
        eel.addAppMsg(msg)

    def start():
        path = os.path.dirname(os.path.abspath(__file__))
        eel.init(path + r"\web", allowed_extensions=[".js", ".html"])
        eel.start(
            "index.html",
            mode="chrome",
            host=str(CHATBOT_HOST),
            port=int(CHATBOT_PORT),
            block=False,
            size=(350, 480),
            position=(10, 100),
            disable_cache=True,
            close_callback=ChatBot.close_callback,
        )
        ChatBot.started = True
        while ChatBot.started:
            try:
                eel.sleep(10.0)
            except:
                break
