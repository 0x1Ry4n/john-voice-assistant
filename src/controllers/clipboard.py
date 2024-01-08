class ClipBoard:
    def __init__(self, keyboard):
        self.keyboard = keyboard

    def copy(self):
        try:
            with self.keyboard.pressed(self.keyboard._Key.ctrl):
                self.keyboard.press("c")
                self.keyboard.release("c")
        except Exception as e:
            print(e)

    def paste(self):
        try:
            with self.keyboard.pressed(self.keyboard._Key.ctrl):
                self.keyboard.press("v")
                self.keyboard.release("v")
        except Exception as e:
            print(e)
