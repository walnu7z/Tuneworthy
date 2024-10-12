from src.Database import *
from src.Rola import *
import os
import time
import re
import fnmatch
import threading
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
        self.total_files = 0
        self.processed_files = 0
        self.mp3_dir_files = []
        self.menas = []
        self.directory = os.path.expanduser(directory)
    
    def prospect(self):
        self.find_mp3_files()

    def find_mp3_files(self):
        """
        Recursively searches through the specified directory and returns a list of all MP3 files found.

        Returns:
            list: A list of paths to MP3 files.
        """
        counter = 0
        for dirpath, dirnames, filenames in os.walk(self.directory):
            self.mp3_dir_files.append([dirpath, []])
            for filename in fnmatch.filter(filenames, '*.mp3'):
                self.mp3_dir_files[-1][1].append(filename)
                counter += 1
        self.total_files = counter

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
                self.processed_files += 1
                if mena_instance:
                    mena_instances.append(mena_instance)

        self.menas = mena_instances

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
            #print(f"Song correctly read at: {filepath}")
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
    def __init__(self, path="~/Music"):
        self.rolas = []
        self.db = MusicLibraryDB()
        self.prospector = Prospector(path)
        self.mining_progress = 0
        self.isExtracting = False
        self.isMining = False
        self.isMining_finished = False


    def mine(self):
        self.prospector.prospect()
        extracting_thread = threading.Thread(target=self.walk_and_extract_dir)
        extracting_thread.start()
        self.isExtracting = True
        if(self.prospector.total_files == 0):
            self.mining_progress = 1
            self.isMining_finished = True
            return
        while(extracting_thread.is_alive and self.isExtracting):
            self.mining_progress = self.prospector.processed_files / self.prospector.total_files
            time.sleep(0.5)
        extracting_thread.join() 

        mining_thread = threading.Thread(target=self.populate_DB)
        mining_thread.start()
        self.isMining = True
        while(mining_thread.is_alive and self.isMining):
            self.mining_progress = self.prospector.processed_files / self.prospector.total_files
            time.sleep(0.5)
        mining_thread.join() 
        self.isMining_finished = True
        print("Rolas agregadas!")

    def walk_and_extract_dir(self):
        self.prospector.pop_and_extract()
        self.isExtracting = False

    def populate_DB(self):
        total = self.prospector.total_files
        current = 0
        for entry in self.prospector.menas:
            self.rolas.append(self.add_entry_from_mena(entry))
            current += 1
            self.mining_progress = current/total
        self.mining_progress = 1
        self.isMining = False
    
    def search(self, query):
        return self.db.execute_query(query)

    def add_entry_from_mena(self, mena: Mena):
        return self.db.add_song(mena.TPE1, mena.TALB, mena.PATH, mena.TIT2, mena.TRCK, mena.TDRC, mena.TCON)

    def close_DB(self):
        self.db.close()


    def search_tokens(self, input_string):
        if input_string == "":
            return

        # Define the valid words (categories)
        valid_words = ["title", "artist", "album", "year", "genre", "track", "t", "a", "d", "y", "g", "n"]
        
        # Regular expression pattern to match WORD:SEARCH_ENTRY
        pattern = r'(?P<word>{}):(?P<entry>(?:"[^"]*"|\S+))'.format("|".join(valid_words))
        just_words = tokenize_single_words(input_string)

        matches = re.finditer(pattern, input_string)

        titles = []
        artists = []
        albums = []
        years = []
        genres = []
        tracks = []
        matched = False
        for match in matches:
            matched = True
            word = match.group("word")
            entry = match.group("entry").strip('"')
            if len(entry) > 0:
                if word == 'title' or word == 't':
                    titles.append(entry)
                elif word == 'artist' or word == 'a':
                    artists.append(entry)
                elif word == 'album' or word == 'd':
                    albums.append(entry)
                elif word == 'year' or word == 'y':
                    years.append(entry)
                elif word == 'genre' or word == 'g':
                    genres.append(entry)
                elif word == 'track' or word == 'n':
                    tracks.append(entry)

        query_tail = ""
        if matched:
            query_tail = string_search_for_all_fields(titles, artists, albums, years, genres, tracks)
        if len(just_words) > 0:
            if matched:
                query_tail = query_tail + " AND "
            query_tail = query_tail + string_search_for_any_field(just_words)
        if matched or len(just_words) > 0:
            query = generate_sql(query_tail) + ';'
            return self.search(query)
        else:
            return



def tokenize_single_words(text):
    def remove_spaces_inside_quotes(match):
        # Get the string inside quotes and remove spaces
        return '"' + match.group(1).replace(' ', '') + '"'
    
    processed_string = re.sub(r'"(.*?)"', remove_spaces_inside_quotes, text)
    tokens = processed_string.split()
    filtered_tokens = [token for token in tokens if '"' not in token and ':' not in token]

    return filtered_tokens


def generate_sql(end):
    query = """SELECT DISTINCT
        rolas.title,
        albums.name AS album_name,
        performers.name AS performer_name,
        rolas.year,
        rolas.genre,
        rolas.track
    FROM rolas
    INNER JOIN albums
        ON rolas.id_album = albums.id_album
    INNER JOIN performers
        ON rolas.id_performer = performers.id_performer
    WHERE
    """

    return query + end

def string_search_for_all_fields(titles, artists, albums, years, genres, tracks):
    conditions = []

    if titles:
        titles_formatted = ' OR '.join(f"rolas.title COLLATE NOCASE LIKE '%{title}%'" for title in titles)
        conditions.append(f"({titles_formatted})")

    if albums:
        albums_formatted = ' OR '.join(f"albums.name COLLATE NOCASE LIKE '%{album}%'" for album in albums)
        conditions.append(f"({albums_formatted})")

    if artists:
        artists_formatted = ' OR '.join(f"performers.name COLLATE NOCASE LIKE '%{artist}%'" for artist in artists)
        conditions.append(f"({artists_formatted})")

    if years:
        years_formatted = ' OR '.join(f"rolas.year COLLATE NOCASE LIKE '%{year}%'" for year in years)
        conditions.append(f"({years_formatted})")

    if genres:
        genres_formatted = ' OR '.join(f"rolas.genre COLLATE NOCASE LIKE '%{genre}%'" for genre in genres)
        conditions.append(f"({genres_formatted})")

    if tracks:
        tracks_formatted = ' OR '.join(f"rolas.track COLLATE NOCASE LIKE '%{track}%'" for track in tracks)
        conditions.append(f"({tracks_formatted})")

    sql_query = ' AND '.join(conditions)
    return '(' + sql_query + ')'

def string_search_for_any_field(input_string):
    # Split the input string into a list of elements, assuming it’s comma-separated
    elements = [elem.strip() for elem in input_string]

    # Create the SQL conditions for each field using LIKE
    conditions = [
        f"rolas.title COLLATE NOCASE LIKE '%{e}%'" for e in elements
    ] + [
        f"albums.name COLLATE NOCASE LIKE '%{e}%'" for e in elements
    ] + [
        f"performers.name COLLATE NOCASE LIKE '%{e}%'" for e in elements
    ] + [
        f"rolas.year COLLATE NOCASE LIKE '%{e}%'" for e in elements
    ] + [
        f"rolas.genre COLLATE NOCASE LIKE '%{e}%'" for e in elements
    ] + [
        f"rolas.track COLLATE NOCASE LIKE '%{e}%'" for e in elements
    ]

    return '(' +  ' OR '.join(conditions) + ')'

    