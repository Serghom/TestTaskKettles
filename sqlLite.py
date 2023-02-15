import sqlite3
from datetime import datetime

class DataBase:
    def __init__(self, nameBase:str): # Конструктор
        self.nameBase = nameBase


    def createConnect(self):
        try:
            self.sqlite_connection = sqlite3.connect(self.nameBase)
            self.cursor = self.sqlite_connection.cursor()
            print("БД создана и успешно подключена")
            sqlite_select_query = "select sqlite_version();"
            self.cursor.execute(sqlite_select_query)
            record = self.cursor.fetchall()
            print("Версия БД SQLite: {}".format(record))
            self.cursor.close()
        except sqlite3.Error as er:
            print("Ошибка при подключении к SQLite: {}".format(er))
        finally:
            if(self.sqlite_connection):
                self.sqlite_connection.close()
                print("Соединение с SQLite закрыто")

    def createTableLog(self):
        try:
            self.sqlite_connection = sqlite3.connect(self.nameBase)
            sqlite_create_table_query = '''CREATE TABLE logs_of_kettles (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                            date datetime, 
                                            log TEXT NOT NULL);'''
            self.cursor = self.sqlite_connection.cursor()
            print("БД подключена к SQLite")
            self.cursor.execute(sqlite_create_table_query)
            self.sqlite_connection.commit()
            print("Таблица успешно создана")
            self.cursor.close()
        except sqlite3.Error as er:
            print("Ошибка при подключении к SQLite: {}".format(er))
        finally:
            if(self.sqlite_connection):
                self.sqlite_connection.close()
                print("Соединение с SQLite закрыто")


    def insertTableValues(self, string:str):
        try:
            self.sqlite_connection = sqlite3.connect(self.nameBase)
            now = datetime.now()

            sqlite_create_table_query = '''INSERT INTO logs_of_kettles (date, log) VALUES (?, ?)'''
            self.cursor = self.sqlite_connection.cursor()
            print("БД подключена к SQLite")
            self.cursor.execute(sqlite_create_table_query, (datetime.now(), string))
            self.sqlite_connection.commit()
            print("Данные успешно добавлены")
            self.cursor.close()
        except sqlite3.Error as er:
            print("Ошибка при подключении к SQLite: {}".format(er))
        finally:
            if(self.sqlite_connection):
                self.sqlite_connection.close()
                print("Соединение с SQLite закрыто")