class Score:
    def __init__(self, name, word, missing, seconds, time): #klassisisesed muutujad
        self.__name = name #mängija nimi
        self.__word = word  #sõna, mida ära arvatakse
        self.__missing = missing #tähed, mis on valesti sisestatud
        self.__seconds = seconds #aeg, sekundites
        self.__time = time #reaalne aeg, mis mängitakse

    #GETTERID
    @property
    def name(self):
        return self.__name

    @property
    def word(self):
        return self.__word

    @property
    def missing(self):
        return self.__missing

    @property
    def seconds(self):
        return self.__seconds

    @property
    def time(self):
        return self.__time
