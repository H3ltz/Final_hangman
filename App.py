import os.path
import sys

from Controller import Controller


class App:
    def __init__(self, db): #kui Äppi luuakse, siis saadakse andmebaasi nimi
        Controller(db_name).main()  #Kui luuakse kontroller, antakse kaasa db_name ja kutsutakse välja main fun.


if __name__ == "__main__": #Kui käivitakse, siis siit läheb käima
    db_name = None #Algselt andmebaasi nime ei ole
    if len(sys.argv) == 2: #Kas käsurea peal on 2 argumenti - üks on failinimi ja teine on andmebaasinimi
        if os.path.exists(sys.argv[1]): #Kas argument on fail
            db_name = sys.argv[1] #andmebaasi nimeks saab käsurealt
    App(db_name) #andmebaasi nimi või käsurealt saadud andmebaasi nimi
