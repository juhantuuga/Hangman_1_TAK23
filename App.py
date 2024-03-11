# App.py
import os.path
import sys
from Controller import Controller


class App:
    def __init__(self, db):
        self.controller = Controller(db)  # Säilita kontrolleri objekt
        self.controller.main()


if __name__ == "__main__":
    db_name = None
    if len(sys.argv) == 2:  # Peab olema kaks argumenti
        if os.path.exists(sys.argv[1]):  # Kas andmebaasifail eksisteerib
            db_name = sys.argv[1]  # Anname db_name väärtuseks antud andmebaasinime
    app = App(db_name)  # Loome äpi, millel on antud andmebaasi nimi
