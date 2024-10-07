from src.Database import *
from src.Rola import *
import os
import re
import fnmatch
from datetime import datetime
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, TRCK

class Mena:
    def __init__(self, PATH, TPE1, TIT2, TALB, TDRC, TCON, TRCK):
        self.PATH = PATH
        self.TPE1 = TPE1  # Lead performer(s)/Soloist(s), el intérprete de la rola.
        self.TIT2 = TIT2  # Title/songname/content description, el título de la rola.
        self.TALB = TALB  # Album/Movie/Show title, el nombre del álbum.
        self.TDRC = TDRC  # Recording time, la fecha de grabación; usualmente el año basta.
        self.TCON = TCON  # Content type, el tipo del contenido; el género.
        self.TRCK = TRCK  # Track number/Position in set, el número de pista o posición.

class Prospector:
    def __init__(self, directory = "~/Music"):
        self.directory = os.path.expanduser(directory)
        self.mp3_dir_files = []
        self.find_mp3_files()

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

    def pop_and_extract(self):
        """Pop an item from mp3_dir_files, extract ID3 data, and return Mena instances."""
        if not self.mp3_dir_files:
            print("No MP3 files found.")
            return []

        # Pop the first directory entry
        mena_instances = []
        while self.mp3_dir_files:
            dirpath, mp3_files = self.mp3_dir_files.pop()
            for filename in mp3_files:
                mena_instance = self.extract_id3v2_tags(dirpath, filename)
                if mena_instance:
                    mena_instances.append(mena_instance)

        return mena_instances

    def extract_id3v2_tags(self, dirpath, filename):
        """Extract ID3v2 tags from an MP3 file and return a Mena instance."""
        filepath = os.path.join(dirpath, filename)
        try:
            audio = MP3(filepath, ID3=ID3)

            TPE1 = self.check_TPE1(audio.tags.get('TPE1', None))
            TIT2 = self.check_TIT2(audio.tags.get('TIT2', None), filename)
            TALB = self.check_TALB(audio.tags.get('TALB', None), filepath)
            TDRC = self.check_TDRC(audio.tags.get('TDRC', None))
            TCON = self.check_TCON(audio.tags.get('TCON', None))
            TRCK = self.check_TRCK(audio.tags.get('TRCK', None))
            
            # Create a Mena instance with extracted data
            print(f"Song correctly read at: {filepath}")
            return Mena(
                PATH=filepath,
                TPE1=TPE1,
                TIT2=TIT2,
                TALB=TALB,
                TDRC=TDRC,
                TCON=TCON,
                TRCK=TRCK
            )
        except Exception as e:
            print(f"Error extracting tags from {filepath}: {e}")
            return None
        
    def check_TPE1(self, value):
        """Check if TPE1 (Lead performer) is not empty; return 'Unknown' if empty."""
        return value.text[0] if value and value.text[0] else 'Unknown'

    def check_TIT2(self, value, filename):
        """Check if TIT2 (Title) is not empty; return filename if empty."""
        return value.text[0] if value and value.text[0] else filename

    def check_TALB(self, value, filepath):
        """Check if TALB (Album) is not empty; return last directory name if empty."""
        if value and value.text[0]:
            return value.text[0]
        dirpath = os.path.dirname(filepath)
        return os.path.basename(dirpath) if dirpath else 'Unknown'

    def check_TDRC(self, value):
        """Check if TDRC (Recording year) is not empty and is an integer; return current year if not."""
        if value and value.text[0].year:
            try:
                year = int(value.text[0].year)
                return year
            except ValueError:
                pass
        return datetime.now().year

    def check_TCON(self, value):
        """Check if TCON (Genre) is not empty; return 'Unknown' if empty."""
        return value.text[0] if value and value.text[0] else 'Unknown'

    def check_TRCK(self, value):
        """Check if TRCK (Track number) is not empty; if it's text, return first consecutive numbers or 0."""
        
        # Try converting the value to an integer directly
        try:
            return int(value)
        except (ValueError, TypeError):
            pass
        
        # Use regex to find the first consecutive digits
        match = re.search(r'\d+', str(value))
        if match:
            return int(match.group(0))
        
        # Return 0 if no valid integer or digits are found
        return 0
            
class Minero:
    def __init__(self):
        self.rolas = []
        self.db = MusicLibraryDB()
        self.populate_DB()
        print("Rolas agregadas!")

    def populate_DB(self):
        prospector = Prospector()
        menas = prospector.pop_and_extract()
        for entry in menas:
            self.rolas.append(self.add_entry_from_mena(entry))

    def add_entry_from_mena(self, mena: Mena):
        return self.db.add_song(mena.TPE1, mena.TALB, mena.PATH, mena.TIT2, mena.TRCK, mena.TDRC, mena.TCON)

    def close_DB(self):
        self.db.close()

    