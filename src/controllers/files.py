import os


class FileHandler:
    def __init__(self):
        self.path = "C://"
        self.files = []
        self.file_exp_status = False

    def list_files(self):
        counter = 0
        self.files = os.listdir(self.path)
        filestr = ""
        for f in self.files:
            counter += 1
            filestr += str(counter) + ":  " + f + "<br>"
        self.file_exp_status = True

        return filestr

    def open_file(self, voice_data):
        if self.file_exp_status == False:
            return None

        counter = 0
        selected_index = int(voice_data.split(" ")[-1]) - 1
        selected_file = os.path.join(self.path, self.files[selected_index])

        if os.path.isfile(selected_file):
            os.startfile(selected_file)
            self.file_exp_status = False
        else:
            try:
                self.path = os.path.join(self.path, self.files[selected_index])
                self.files = os.listdir(self.path)
                filestr = ""
                for f in self.files:
                    counter += 1
                    filestr += str(counter) + ":  " + f + "<br>"

                return filestr
            except Exception as e:
                print(e)
                return -1

    def back(self):
        if self.file_exp_status is False:
            return

        filestr = ""

        a = self.path.split("//")[:-2]
        self.path = "//".join(a)
        self.path += "//"
        self.files = os.listdir(self.path)
        for f in self.files:
            counter += 1
            filestr += str(counter) + ":  " + f + "<br>"

        return filestr
