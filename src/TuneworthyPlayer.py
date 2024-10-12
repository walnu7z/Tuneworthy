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
        self.minero = None
        self.path = "~/Music"
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


        self.stack = self.builder.get_object("stack") 
        self.stack_switcher = self.builder.get_object("stack_switcher")
        self.mining_label = self.builder.get_object("mining_label")
        self.mining_percentage = self.builder.get_object("mining_percentage")
        self.mining_progress_bar = self.builder.get_object("mining_progress_bar") 
        self.search_entry = self.builder.get_object("search_entry")

        self.import_dir_button = self.builder.get_object('import_dir')
        self.dialog = self.builder.get_object('set_path_dialog')
        self.dir_path_label = self.builder.get_object('dir_path')
        self.set_path_button = self.builder.get_object('set_path')
        self.dir_path_label = self.builder.get_object('path_label')


        # Connect signals
        self.import_dir_button.connect('clicked', self.on_import_dir_clicked)
        self.set_path_button.connect('clicked', self.on_set_path_clicked)
        

        # Connect signals
        self.search_entry.connect("activate", self.on_activate_search)
        self.search_entry.connect("search-changed", self.on_search_changed)
        self.search_entry.connect("search-started", self.on_search_started)
        self.search_entry.connect("stop-search", self.on_stop_search)

        # Show the window
        self.win.connect("destroy", self.on_window_destroy)
        self.win.present()

    def on_window_destroy(self, widget):
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

    def on_click_Mine(self, button):
        self.switch_to_mining_stack_page()
        start_mining_thread = threading.Thread(target=self.start_mining)
        start_mining_thread.start()
        self.isMined = True
        button.set_sensitive(False)

    def initialize_mining(self, path):
        self.minero = Minero(path)

    def start_mining(self):
        self.initialize_mining(self.path)
        minero = self.minero
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
        songs  = self.minero.search_tokens(search_entry.get_text())
        self.show_searched_songs(songs)


    def on_search_started(self, search_entry):
        print("Search started")

    def on_stop_search(self, search_entry):
        print("Search stopped")

    def on_import_dir_clicked(self, button):
        # Show the dialog
        self.dialog.show()

    def on_set_path_clicked(self, button):
        # Get the text from the editable label
        path = self.dir_path_label.get_text()

        # Verify the provided path
        if os.path.isdir(os.path.expanduser(path)):
            print(f"Path verified: {path}")
            self.path = path  # Store the path in self.path
            self.dialog.hide()  # Hide the dialog
        else:
            print(f"Invalid path: {path}")

