import sys
import gi
import threading
import re
from src.Minero import *

gi.require_version("Gtk", "4.0")
gi.require_version('Gst', '1.0')
gi.require_version('Adw', '1')
from gi.repository import GLib, Gtk, Gio, Adw, GObject, Gst


class TuneworthyPlayer(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.songs = None
        self.searched_songs = None
        self.isMined = False
        self.connect('activate', self.on_activate)


    def on_activate(self, app):
        # Load the UI from the .ui file
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./src/tuneworthy.ui")  # Adjust the path if necessary

        # Get the main window object from the UI file
        self.win = self.builder.get_object("window")  # Make sure the ID matches your UI file
        self.win.set_application(app)  # Set the application for the window

        #self.builder.connect_signals(self)        

        self.song_liststore = self.builder.get_object("model_list") 

        button = self.builder.get_object("mine_button")

        if True:
            button.set_sensitive(True)  # Disables the button

        # Connect the button to a callback function
        button.connect("clicked", self.on_click_Mine)


        self.stack = self.builder.get_object("stack")  # Replace with your actual GtkStack ID
        self.stack_switcher = self.builder.get_object("stack_switcher")
        self.mining_label = self.builder.get_object("mining_label")
        self.mining_percentage = self.builder.get_object("mining_percentage")
        self.mining_progress_bar = self.builder.get_object("mining_progress_bar") 
        self.search_entry = self.builder.get_object("search_entry")

        # Connect signals
        self.search_entry.connect("activate", self.on_activate_search)
        self.search_entry.connect("search-changed", self.on_search_changed)
        self.search_entry.connect("search-started", self.on_search_started)
        self.search_entry.connect("stop-search", self.on_stop_search)

        # Show the window
        self.win.connect("destroy", self.on_window_destroy)
        self.win.present()

    def on_window_destroy(self, widget):
        # Quit the application when the window is closed
        self.quit()

    def switch_to_songs_stack_page(self):
        """Switch to the mining page in the GtkStack."""
        songs_page = self.builder.get_object("songs_page")
        songs_page_box = songs_page.get_child()  
        self.stack.set_visible_child(songs_page_box)

    def switch_to_mining_stack_page(self):
        """Switch to the mining page in the GtkStack."""
        mining_page = self.builder.get_object("mining_page")
        mining_page_box = mining_page.get_child()  
        self.stack.set_visible_child(mining_page_box)

    def update_mining_label(self, text):
        """Update the text of the mining_label."""
        self.mining_label.set_label(text)

    def update_mining_percentage(self, percentage):
        """Update the text of the mining_percentage label and make it visible."""
        self.mining_percentage.set_visible(True)
        self.mining_percentage.set_label(f"{percentage*100:.2f}%")


    def update_mining_progress_bar(self, value):
        """Update the value of the mining progress bar."""
        self.mining_progress_bar.set_value(value)  # Assuming value is between 0 and 100

    #@Gtk.Template.Callback
    def on_click_Mine(self, button):
        self.switch_to_mining_stack_page()
        start_mining_thread = threading.Thread(target=self.start_mining)
        start_mining_thread.start()
        self.isMined = True
        button.set_sensitive(False)

    def start_mining(self):
        minero = Minero()
        miner_thread = threading.Thread(target=minero.mine)
        miner_thread.start()
        while(miner_thread.is_alive and not minero.isMining_finished):
            if(minero.isExtracting):
                self.update_mining_label("Walking dir...")
            elif(minero.isMining):
                self.update_mining_label("Mining data...")
            self.update_mining_percentage(minero.mining_progress)
            self.update_mining_progress_bar(minero.mining_progress)
            time.sleep(0.1)
        self.update_mining_label("Finished!")
        self.songs = minero.rolas
        miner_thread.join()  # This will block until the thread has finished
        self.show_all_songs()
        self.switch_to_songs_stack_page()

    def show_all_songs(self):
        self.song_liststore.remove_all()
        for song in self.songs:       
            # Add the song instance to the song_liststore
            self.song_liststore.append(song)
        
    def show_searched_songs(self, search_results):
        self.song_liststore.remove_all()  
        for song in search_results: 
            self.song_liststore.append(song)
 
    def on_activate_search(self, search_entry):
        print("Search activated")

    def on_search_changed(self, search_entry):
        if (not self.isMined):
            return
        if search_entry.get_text().strip()=="":    
            self.show_all_songs()
            return
        print(f"Search text changed: {search_entry.get_text()}")
        songs  = self.search_tokens(search_entry.get_text())
        self.show_searched_songs(songs)


    def on_search_started(self, search_entry):
        print("Search started")

    def on_stop_search(self, search_entry):
        print("Search stopped")

    def search_tokens(self,input_string):
        if input_string == "":
            return

        # Define the valid words (categories)
        valid_words = ["title", "artist", "album", "year", "genre", "track", "t", "a", "d", "y", "g", "n"]
        
        # Regular expression pattern to match WORD:SEARCH_ENTRY
        pattern = r'(?P<word>{}):(?P<entry>(?:"[^"]*"|\S+))'.format("|".join(valid_words))
        #words = input_string.split()
        just_words = tokenize_single_words(input_string)

        # Find all matches in the input string
        matches = re.finditer(pattern, input_string)

        # Print each token with its correct category
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
            entry = match.group("entry").strip('"')  # Remove quotes if present
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
                #print(f"{word.capitalize()}: {entry}")

        query_tail = ""
        if matched:
            query_tail = string_search_for_all_fields(titles, artists, albums, years, genres, tracks)
        if len(just_words) > 0:
            if matched:
                query_tail = query_tail + " AND "
            query_tail = query_tail + string_search_for_any_field(just_words)
        if matched or len(just_words) > 0:
            query = generate_sql(query_tail) + ';'
            minero = Minero()
            return minero.search(query)
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

    # Join all conditions with ' AND '
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

    # Join all conditions with ' OR '
    return '(' +  ' OR '.join(conditions) + ')'
