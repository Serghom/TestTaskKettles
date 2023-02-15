from json import load
from Kettle import Kettles
from Report import LogFile
from sqlLite import DataBase
from os import system, name
import keyboard
from time import time
from art import tprint


def clearConsole():
    # Если это Windows
    if (name == "nt"):
        _ = system("cls")
    else:
        # Если это *nix системы или MacOS
        _ = system("clear")


def is_digit(string:str) -> bool:
    # Если это int > 0
    if(string.isdigit()):

        return True
    else:
        try:
            # Попытаться перевести строку в float
            float(string)

            return True
        except ValueError:

            # Если не получиться, то вернуть False
            return False


def readJsonFile():
    with open("kettle_settings.json") as js:
        kettles = load(js)

    return kettles["kettles"]


def setKettles(kettle):
    # Читаем данные из json документа и инициализируем ими объекты класса Kettles
    name_kettle = kettle["name"]
    boiling_time = kettle["characteristics"]["boiling_time"]
    switch_off_temp = kettle["characteristics"]["switch_off_temp"]
    water_volume = kettle["characteristics"]["water_volume"]

    return Kettles(name_kettle, int(boiling_time), float(switch_off_temp), float(water_volume))


def printMenu() -> int:
    # По очереди выводим характеристики чайников
    print("Выберите чайник:\n=================================")
    for i, ket in enumerate(list_of_kettles):
        print("Номер: {}".format(i))
        ket.getCharacteristics()

    # Запоминаем какой чайник выбрал пользователь
    number = input("Введите номер чайника: ")
    # Проверяем введенное пользователем на валидность
    if(is_digit(number)):
        if(int(number) > len(list_of_kettles) - 1):
            clearConsole()
            print("Такого чайника нет, попробуйте снова")

            return -1
        else:
            # Если пользователь ввел все верно, то возвращаем это значение
            return int(number)
    else:
        clearConsole()
        print("Это не число, попробуйте снова")

        return -1


def pourWater(number:int):
    print("\n=================================\n"
          "Сколько залить в чайник \"{}\", "
          "Объем чайника: {}л".format(list_of_kettles[number].getName(),
                                     list_of_kettles[number].getWaterVolume()))
    volume = input("Введите объем воды: ")
    db.insertTableValues("Пользователь залил {}л из {}л возможных".format(volume, list_of_kettles[number].getWaterVolume()))
    log.write("Пользователь залил {}л из {}л возможных".format(volume, list_of_kettles[number].getWaterVolume()))

    # Проверяем введенное пользователем на валидность
    if(is_digit(volume)):
        # В случае успеха записываем в параметры объекта
         if(not list_of_kettles[number].pour_the_kettle(float(volume))):
             clearConsole()
             print("Вы заливаете слишком мало или слишком много, попробуйте снова")
             pourWater(number)

    else:
        clearConsole()
        print("Это не число, попробуйте снова")
        pourWater(number)


def startBoiling(number:int): # Включить чайник
    db.insertTableValues("Пользователь нажал Ctrl+B чтобы включить чайник")
    log.write("Пользователь нажал Ctrl+B чтобы включить чайник")
    list_of_kettles[number].setState(True)
    list_of_kettles[number].boilingWater()


def stopBoiling(number:int): # Выключить чайник
    db.insertTableValues("Пользователь нажал Ctrl+E чтобы включить чайник")
    log.write("Пользователь нажал Ctrl+E чтобы выключить чайник")
    list_of_kettles[number].setState(False)
    list_of_kettles[number].getControlState()


def controlMenu(number:int):
    # Устанавливаем сочитания клавиш
    keyboard.add_hotkey("Ctrl + b", startBoiling, args=(number, ))
    keyboard.add_hotkey("Ctrl + e", stopBoiling, args=(number, ))

    # Выводим информацию о состояние чайника
    list_of_kettles[number].getControlState()
    if (list_of_kettles[number].getState()):
        print("Ctrl + e Что-бы выключить")
    else:
        print("Ctrl + b Что-бы включить")

    done = True
    while(done):
        timing = time()
        # Ждем когда пользователь включит чайник
        keyboard.wait("Ctrl + b")
        db.insertTableValues("Температура чайника {}".format(round(list_of_kettles[number].getTemperature(), 2)))
        log.write("Температура чайника {}".format(round(list_of_kettles[number].getTemperature(), 2)))
        while(list_of_kettles[number].getState()):
            # Каждую секунду обновляем состояние чайника
            if(time() - timing > 1):
                timing = time()
                list_of_kettles[number].boilingWater()
                db.insertTableValues(
                    "Температура чайника {}".format(round(list_of_kettles[number].getTemperature(), 2)))
                log.write("Температура чайника {}".format(round(list_of_kettles[number].getTemperature(), 2)))
                if (list_of_kettles[number].getState()):
                    print("Ctrl+E Что-бы выключить")
                else:
                    print("Ctrl+B Что-бы включить")

        # Когда основной цикл закончится, завершить внешний, изначально это делалось для того,
                                                    # чтобы можно было включить чайник повторно
        if(list_of_kettles[number].getState()):
            pass
        else:
            if (round(list_of_kettles[number].getTemperature(), 2) >= list_of_kettles[number].getSwitchOffTemp()):
                db.insertTableValues("Чайник закипел")
                log.write("Чайник закипел")
                done = False
            elif (list_of_kettles[number].getTemperature() > list_of_kettles[number].getStandartTempWater() and
                  list_of_kettles[number].getTemperature() < list_of_kettles[number].getSwitchOffTemp()):
                done = False

    clearConsole()
    list_of_kettles[number].getControlState()
    db.insertTableValues("Температура чайника {}".format(round(list_of_kettles[number].getTemperature(), 2)))
    log.write("Температура чайника {}".format(round(list_of_kettles[number].getTemperature(), 2)))

if __name__ == '__main__':
    tprint("-= The    Kettles =-")
    # Создаем объект для записи логов
    log = LogFile("report.txt")

    db = DataBase("the_kittles_data_base_log.db")
    db.createConnect()
    db.createTableLog()

    # Записываем сообщение в логи
    db.insertTableValues("Запуск программы")
    log.write("Запуск программы\n===================================")

    list_of_kettles = []
    # Читаем конфигурационный файл
    for kettle in readJsonFile():
        # Записываем чайнки в лист
        list_of_kettles.append(setKettles(kettle))

    # Выводим меню пользователя и запоминаем выбранный чаник
    number = printMenu()
    # Записываем сообщение в логи
    db.insertTableValues("Пользователь выбрал чайник № {}".format(number))
    log.write("Пользователь выбрал чайник № {}".format(number))

    while(number == -1):
        number = printMenu()
        db.insertTableValues("Пользователь выбрал чайник № {}".format(number))
        log.write("Пользователь выбрал чайник № {}".format(number))

    # Отчищаем консоль вывода
    clearConsole()
    # Заполняем выбранный чаник
    pourWater(number)
    # Выводим меню управления чайником
    controlMenu(number)
    db.insertTableValues("Завершение выполнения программы")
    log.write("Завершение выполнения программы")
    # log.closeFile()

