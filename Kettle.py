from os import system, name
from art import tprint

class Kettles:
    def __init__(self, name:str, boiling_time:int, switch_off_temp:float, water_volume:float): # Конструктор
        self.name = name                            # Название чаника
        self.boiling_time = boiling_time            # Время закипания
        self.switch_off_temp = switch_off_temp      # Температура выключения
        self.water_volume = water_volume            # Объем воды

        self.water_filling = 0                      # Заполнение водой
        self.state = False                          # Состояние (вкл/выкл)
        self.water_temp = 14                        # Температура воды
                                                        # (0 - лед, холодная вода из под крана должна быть < 20°C)
        self.standart_temp_water = self.water_temp  # Стандартная температура воды

    def getName(self) -> str:   # Получить название чайника
        return self.name

    def getWaterVolume(self) -> float:  # Получить объем чайника
        return self.water_volume

    def getWaterFilling(self) -> float: # Получить кол-во залитой воды
        return self.water_filling

    def getState(self) -> bool: # Получить состояние (вкл/выкл)
        return self.state

    def getTemperature(self) -> float: # Получить температуру воды в чайнике
        return self.water_temp

    def getSwitchOffTemp(self) -> float: # Получить температуру выключения чайника
        return self.switch_off_temp

    def getBoilingTime(self) -> int: # Получить время закипания воды
        return self.boiling_time

    def getStandartTempWater(self) -> float: # Получить изначальную температуру воды
        return self.standart_temp_water


    def getCharacteristics(self) -> None: # Вывод характеристик чайника
        print("Название: {}\n"
              "| Время закипания: {} cек\n"
              "| Температура выключения: {}°C\n"
              "| Объем: {}л\n=================================".format(self.name, self.boiling_time,
                                                                       self.switch_off_temp, self.water_volume))

    def getControlState(self) -> None:
        self.clearConsole()
        if (self.getState()):
            state = "Включен"
        else:
            if(round(self.water_temp, 2) >= self.switch_off_temp):
                state = "Вскипел"
            elif(self.water_temp > self.standart_temp_water and self.water_temp < self.switch_off_temp):
                state = "Остановлен"
            else:
                state = "Выключен"
        print("====================================\n"
              "Название:   \"{}\"\n"
              "Состояние:   {}\n"
              "Залито:      {}л\n"
              "Температура: {}°C\n"
              "====================================\n".format(self.name, state,
                                                              self.water_filling, round(self.water_temp, 2)))

    def setState(self, switch:bool) -> None: # Задать состояние чайника (вкл/выкл)
        self.state = switch

    def pour_the_kettle(self, volume:float) -> bool:    # Заполнение чаника водой
        if(volume <= 0.0001 or volume > self.water_volume):
            return False
        else:
            self.water_filling = volume
            return True

    def boilingWater(self) -> None:
        if(self.state):
            one_step_temp = (self.switch_off_temp - self.standart_temp_water)/self.boiling_time
            if(round(self.water_temp, 2) + one_step_temp <= self.switch_off_temp):
                self.water_temp += one_step_temp

            if(round(self.water_temp, 2)  >= self.switch_off_temp):
                self.state = False
            else:
                self.getControlState()

    def clearConsole(self) -> None:
        if (name == "nt"):
            _ = system("cls")
        else:
            _ = system("clear")