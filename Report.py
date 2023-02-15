import os.path
from datetime import datetime

class LogFile:
    def __init__(self, filename:str): # Конструктор
        self.filename = filename



    def write(self, string:str) -> None:
        if(os.path.exists(self.filename)):
            self.file = open(self.filename, 'a')
        else:
            self.file = open(self.filename, 'w')
        now = datetime.now()
        self.file.write(now.strftime("%Y-%m-%d %H:%M:%S") + " | " + string + "\n")

        self.file.close()

