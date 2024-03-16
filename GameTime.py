import time


class GameTime:
    def __init__(self, lbl_time ): #Objektile antakse kaasa label, kus peab aeg hakkab jooksma
        self.__lbl_time = lbl_time
        self.__counter = 0 #Mänguaeg, aeg hakkab 0-st
        self.__running = False #Kas aeg käib

    #GETTERID
    @property
    def counter(self):
        return self.__counter

    def update(self):
        if self.__running: #Kui aeg jookseb
            if self.__counter == 0:
                display = '00:00:00'
            else: #Näitab hetke mängu aega
                display = time.strftime('%H:%M:%S', time.gmtime(self.__counter))

            self.__lbl_time['text'] = display #Määrab labelil oleva teksti
            self.__lbl_time.after(1000, self.update) #Iga sekund kutsutakse välja
            self.__counter += 1 #Suureneb counter (uuendab label teksti iga sekundi tagant)

    def start(self):
        self.__running = True
        self.update() #Kutsub update-i välja

    def stop(self): #Aeg enam ei jookse
        self.__running = False

    def reset(self): #Määrab uue aja
        self.__counter = 0
        self.__lbl_time['text'] = '00:00:00'

