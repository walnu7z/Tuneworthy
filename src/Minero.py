from src.Database import *
import os
import fnmatch

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
    def __init__(self, directory = "~/Music"):
        self.directory = os.path.expanduser(directory)
        self.mp3_dir_files = []

    def find_mp3_files(self):
        """
        Recursively searches through the specified directory and returns a list of all MP3 files found.

        Returns:
            list: A list of paths to MP3 files.
        """
        for dirpath, dirnames, filenames in os.walk(self.directory):
            self.mp3_dir_files.append([dirpath, []])
            for filename in fnmatch.filter(filenames, '*.mp3'):
                self.mp3_dir_files[-1][1].append(filename)

class Minero:
    def __init__(self):
        self.db = MusicLibraryDB()

    def add_entry_from_mena(self, mena: Mena):
        self.db.add_entry(mena.TPE1, mena.TALB, mena.PATH, mena.TIT2, mena.TRCK, mena.TDRC, mena.TCON)

    def close_DB(self):
        self.db.close()

    