from src.Database import *
import os

class Mena:
    def __init__(self, PATH, TPE1, TIT2, TALB, TDRC, TCON, TRCK):
        self.PATH = PATH
        self.TPE1 = TPE1  # Lead performer(s)/Soloist(s), el intérprete de la rola.
        self.TIT2 = TIT2  # Title/songname/content description, el título de la rola.
        self.TALB = TALB  # Album/Movie/Show title, el nombre del álbum.
        self.TDRC = TDRC  # Recording time, la fecha de grabación; usualmente el año basta.
        self.TCON = TCON  # Content type, el tipo del contenido; el género.
        self.TRCK = TRCK  # Track number/Position in set, el número de pista o posición.
        self.ID_TPE1 = None
        self.ID_TALB = None

class Prospector:
    def __init__(self, name):
        self.name = name

class Minero:
    def __init__(self):
        self.db = MusicLibraryDB()

    def display_info(self):
        return f"TPE1: {self.TPE1}\nTIT2: {self.TIT2}\nTALB: {self.TALB}\nTDRC: {self.TDRC}\nTCON: {self.TCON}\nTRCK: {self.TRCK}"

    def add_entry_from_mena(self, mena: Mena):
        self.db.add_entry(mena.TPE1, mena.TALB, mena.PATH, mena.TIT2, mena.TRCK, mena.TDRC, mena.TCON)

    def close_DB(self):
        self.db.close()