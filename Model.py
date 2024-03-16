import glob
import sqlite3
from datetime import datetime

from Score import Score


class Model:
    def __init__(self):
        self.__database = 'databases/hangman_words_ee.db' #andmebaasi nimi databases kaustast
        #pip install Pillow > et saaks piltidega toimetada
        self.__image_files = glob.glob('images/*.png') #List mängu piltidega
        self.__random_word = ""  # juhuslik sõna
        self.__all_letters = []  # kõik sisestatud tähed
        self.__wrong_letters = []  # valed tähed
        self.__correct_letters = []  # õigsed tähed
        self.__error_count = 0
        self.__guessed_letters = []

    #GETTERID
    @property
    def database(self):
        return self.__database

    @property
    def image_files(self):
        return self.__image_files

    @property
    def random_word(self):
        return self.__random_word

    @property
    def all_letters(self):
        return self.__all_letters

    @property
    def wrong_letters(self):
        return self.__wrong_letters

    @property
    def correct_letters(self):
        return self.__correct_letters

    @property
    def guessed_letters(self):
        return self.__guessed_letters

    @property
    def error_count(self):
        return self.__error_count

    #SETTERID
    @database.setter
    def database(self, value):
        self.__database = value

    #Loeb andmebaasi tabelist Edetabel kõik kirjed, andmebaasi ühendus
    def read_scores_data(self):
        connection = None
        try:
            connection = sqlite3.connect(self.__database)
            sql = 'SELECT * FROM scores ORDER BY seconds;'
            cursor = connection.execute(sql)
            data = cursor.fetchall()
            result = []
            for row in data:
                result.append(Score(row[1], row[2], row[3], row[4], row[5])) #nimi, word, missing, seconds, time

            return result
        except sqlite3.Error as error: #aind errrori puhul
            print(f'Viga ühenduda andmebaasi{self.__database}: {error}')
        finally: #tehakse alati
            if connection: #kui ühendus püsib, tuleb alati sulgeda
                connection.close()

    #Meetod, mis seadistab uue mängu
    def new_game(self):
        self.__random_word = self.get_random_word_from_database()  # uue sõna seadistamine
        self.__wrong_letters = []  # seadistab muutuja algväärtuse
        self.__correct_letters = []  # seadistab muutuja algväärtuse
        self.__all_letters = []
        self.__guessed_letters = list('_' for _ in self.__random_word)  # iga tähe asemel algkriips
        self.__error_count = 0

    #Meetod, mis seadistab juhusliku sõna
    def get_random_word_from_database(self):  # andmebaasi ühendus
        global word
        connection = None
        try:
            connection = sqlite3.connect(self.__database)
            sql = "SELECT word FROM words ORDER BY RANDOM() LIMIT 1"
            cursor = connection.execute(sql)
            word = cursor.fetchone()[0]
            connection.close()
            return word
        except sqlite3.Error as error:  # aind errrori puhul
            print(f'Viga ühenduda andmebaasi{self.__database}: {error}')
        finally:  # tehakse alati
            if connection:  # kui ühendus püsib, tuleb alati sulgeda
                connection.close()

     #Kasutaja sisestatuse kontroll
    def validate_input(self, letter):
        if letter:
            my_letter = letter[0].lower()
            self.__all_letters.append(my_letter)
            for index, char in enumerate(self.__random_word):
                if char.lower() == my_letter:
                    self.__correct_letters.append(my_letter)
                    self.__guessed_letters[index] = my_letter
            if my_letter not in list(self.__random_word.lower()):
                self.__wrong_letters.append(my_letter)
                self.__error_count += 1

    #Tagastab tulemuse stringina.
    def format_letters(self, letter):
        return ', '.join(letter)

    #Lisab mängija info andmebaasi
    def save_data(self, name, game_time):
        name = name.strip()
        connection = None
        try:
            connection = sqlite3.connect(self.__database)
            sql = 'INSERT INTO scores (name, word, missing, seconds, date_time) VALUES (?, ?, ?, ?, ?)'
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor = connection.execute(sql, (name, self.__random_word, self.format_letters(self.__wrong_letters), game_time, time))
            connection.commit()
        except sqlite3.Error as error:  # aind errrori puhul
            print(f'Viga ühenduda andmebaasi{self.__database}: {error}')
        finally:  # tehakse alati
            if connection:  # kui ühendus püsib, tuleb alati sulgeda
                connection.close()
