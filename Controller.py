import sqlite3
from tkinter import messagebox, simpledialog

from GameTime import GameTime
from Model import Model
from View import View


class Controller:
    def __init__(self, db_name=None): #Andmebaasi nimi tuleb kaasa
        #objektid luuakse controlleris
        self.__model = Model()
        self.__view = View(self, self.__model)
        if db_name is not None: #kui nimi on olemas
            self.__model.database = db_name
        self.__game_time = GameTime(self.__view.lbl_time)
        #print(self.__model.database) #näitab konsoolis andmebaasi nime
        #Terminalis > py. /App.py ./databases/hangman_words_en.db = kasutab seda andmebaasi, mis käsurealt (teistpidi kaldkriipsud)

    def main(self):
        self.__view.main()

    def btn_scoreboard_click(self): #Edetabeli nupu vajutamine
        window = self.__view.create_scoreboard_window()
        data = self.__model.read_scores_data()
        self.__view.draw_scoreboard(window, data)

    #Kui möngu ei ole(mäng lõppes või katkes), siis nupud/sisestuskast aktiivsed/mitteaktiivsed
    def buttons_no_game(self):
        self.__view.btn_new['state'] = 'normal'
        self.__view.btn_cancel['state'] = 'disabled'
        self.__view.btn_send['state'] = 'disabled'
        self.__view.char_input.delete(0, 'end') #Sisestuskast tühjaks
        self.__view.char_input['state'] = 'disabled'

    #Kui Mäng algab (vajutatakse btn_new)
    def buttons_to_game(self):
        self.__view.btn_new['state'] = 'disabled'
        self.__view.btn_cancel['state'] = 'normal'
        self.__view.btn_send['state'] = 'normal'
        self.__view.char_input['state'] = 'normal'
        self.__view.char_input.focus() #kohe saab sisestuskasti kirjutada

    #Uus möng
    def btn_new_click(self):
        self.buttons_to_game() #kutsutakse välja

        #Muuda pilti id-ga 0
        self.__view.change_image(0)

        #Seadista mudelis uus mäng
        self.__model.new_game()

        #Näita äraarvatavat sõna aga iga tähe asemel on allkriips
        self.__view.lbl_result['text'] = self.__model.correct_letters
        self.__view.lbl_error['text'] = 'Vigased tähed'

        #Mängu aeg resettda ja uuesti käima panna
        self.__game_time.reset()
        self.__game_time.start()

    #Loobutakse möngust
    def btn_cancel_click(self):
        self.__game_time.stop() #aeg seisma
        self.buttons_no_game()
        self.__view.change_image(len(self.__model.image_files)-1)

    #Saada nuppu funktsionaalsus
    def btn_send_click(self):
        #print(self.__view.char_input.get())
        guess = self.__view.char_input.get()
        self.__model.validate_input(guess)  #suuna mudelisse infot töötlema
        self.__view.char_input.delete(0, 'end') #Muuda teksti Vigased tähed
        self.__view.lbl_result['text'] = " ".join(self.__model.guessed_letters).upper() #Muuda teksti tulemus aknas (äraarvatav sõna)
        self.__view.lbl_error['text'] = f'Vigased tähed: {self.__model.format_letters(self.__model.wrong_letters)}' #Muuda teksti Vigased tähed
        if self.__model.error_count > 0:
            self.__view.lbl_error['fg'] = 'red'
        self.__view.change_image(self.__model.error_count)
        self.game_over() #mäng on läbi

    def game_over(self):
        is_game_over = False
        game_won = False

        if self.__model.error_count == 11:
            is_game_over = True
            messagebox.showwarning('KAOTUS', "MÄNG ON LÄBI")

        if self.__model.random_word.lower() == ''.join(self.__model.guessed_letters).lower():
            game_won = True
            is_game_over = True

        if is_game_over:
            self.__game_time.stop()  #peata mänguaeg
            self.buttons_no_game() #seadistada nupud õigeks
        if game_won:
            name = simpledialog.askstring('VÕIT','Sisesta mängija nimi: ')
            if name:
                self.__model.save_data(name, self.__game_time.counter)
