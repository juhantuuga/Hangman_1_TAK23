import glob
import sqlite3
from datetime import datetime

from Score import Score


class Model:
    def __init__(self):  # Seadistame klassi
        self.__database = 'databases/hangman_words_ee.db'
        self.__image_files = glob.glob('images/*.png')
        self.__word = ''  # Praegune sõna
        self.__letters = []  # Mitu tähte on kasutaja sisestanud
        self.__wrong_count = 0  # Mitu valesti on läinud
        self.__correct_letters = []  # Millised on õiged tähed olnud
        self.__wrong_letters = []  # Millised on valed tähed olnud

    # Ligipääsud klassiomadustele:
    @property
    def database(self):
        return self.__database

    @property
    def image_files(self):
        return self.__image_files

    @property
    def word(self):
        return self.__word

    @property
    def correct_letters(self):
        return self.__correct_letters

    @property
    def wrong_letters(self):
        return self.__wrong_letters

    @property
    def wrong_count(self):
        return self.__wrong_count

    @database.setter
    def database(self, value):
        self.__database = value

    def read_scores_data(self):  # Loeb skoori andmed ja tagastab need
        connection = None
        try:  # Proovime andmebaasiga ühendust saada
            connection = sqlite3.connect(self.__database)
            sql = 'SELECT * FROM scores ORDER BY seconds;'
            cursor = connection.execute(sql)
            data = cursor.fetchall()
            result = []
            for row in data:
                result.append(Score(row[1], row[2], row[3], row[4], row[5]))
            return result
        except sqlite3.Error as error:  # Mis siis kui ei saa ühendust
            print(f'Viga andmebaasi {self.__database} ühendamisel: {error}')
        finally:
            if connection:
                connection.close()  # Sulgeme ühenduse

    def new_game(self):  # Uus mäng, uus sõna
        self.__wrong_count = 0
        self.__letters = []
        self.__correct_letters = []
        self.__wrong_letters = []
        self.__word = self.random_word()  # Suvaline sõna listist
        self.__correct_letters = list("_" * len(self.__word))  # Asendame uue sõna allkriipsudega

    def random_word(self):  # Meetod uue sõna valimiseks
        connection = None
        try:
            connection = sqlite3.connect(self.__database)
            sql = 'SELECT word FROM words ORDER BY RANDOM() LIMIT 1;'  # Üks sõna suvaliselt
            cursor = connection.execute(sql)
            word = cursor.fetchone()[0]
            cursor.close()
            return word  # Annab sõna
        except sqlite3.Error as error:  # Kui mingi error tekib
            print(f'Viga andmebaasi {self.__database} ühendamisel: {error}')
        finally:
            if connection:
                connection.close()

    def check_user_input(self, text):  # Kasutaja sisestuse kontroll ja lugemine (mitu valesti ja mitu õigesti)
        if text:
            guess = text[0].strip().lower()  # Teeme tähe arvutile lihtsamaks
            self.__letters.append(guess)  # Lisame tähe olemasolevasse listi, mida kasutaja on pakkunud
            word_letters = list(self.__word.lower())  # Teeme listi, mis näitab kasutaja pakutud tähti
            if guess in word_letters:  # Kui täht on sõnas olemas, siis...
                for index, letter in enumerate(word_letters):  # Käib kogu sõna üle
                    if guess == letter:  # Kui pakutud täht vastab sõna tähele, siis...
                        self.__correct_letters[index] = guess  # Asendab allkriipsu õige tähega
            else:  # Kui kasutaja ebaõnnestub, siis...
                self.__wrong_count += 1
                if guess in self.__letters and guess not in self.__wrong_letters:  # Järelikult on juba proovitud
                    self.__wrong_letters.append(guess)

    def list_to_string(self, char_list):  # Sulatab listi stringiks
        return ''.join(char_list)

    def save_score(self, name, game_time):  # Salvestame skoori andmebaasi ja paneme ta pärast ka lukku
        name = name.strip()  # Kustutame üleliigse nimelt
        connection = None
        try:
            connection = sqlite3.connect(self.__database)
            today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = 'INSERT INTO scores (name, word, missing, seconds, date_time) VALUES (?, ?, ?, ?, ?)'
            connection.execute(sql, (
                name.title(),
                self.__word.upper(),
                self.list_to_string(self.__wrong_letters).upper(),
                game_time,
                today
            ))
            connection.commit()
        except sqlite3.Error as error:
            print(f'Viga andmebaasi {self.__database} ühendamisel: {error}')
        finally:
            if connection:
                connection.close()
