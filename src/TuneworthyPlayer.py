import sys
import gi
import threading
from src.Minero import *

gi.require_version("Gtk", "4.0")
gi.require_version('Gst', '1.0')
gi.require_version('Adw', '1')
from gi.repository import GLib, Gtk, Gio, Adw, GObject, Gst


class TuneworthyPlayer(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.songs = None
        self.connect('activate', self.on_activate)


    def on_activate(self, app):
        # Load the UI from the .ui file
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./src/tuneworthy.ui")  # Adjust the path if necessary

        # Get the main window object from the UI file
        self.win = self.builder.get_object("window")  # Make sure the ID matches your UI file
        self.win.set_application(app)  # Set the application for the window

        self.song_liststore = self.builder.get_object("model_list") 

        button = self.builder.get_object("mine_button")

        if True:
            button.set_sensitive(True)  # Disables the button

        # Connect the button to a callback function
        button.connect("clicked", self.on_click_Mine)


        self.stack = self.builder.get_object("stack")  # Replace with your actual GtkStack ID
        self.stack_switcher = self.builder.get_object("stack_switcher")
        self.mining_page = self.builder.get_object("mining_page")
        self.mining_page_box = self.mining_page.get_child()  
        self.mining_label = self.builder.get_object("mining_label")
        self.mining_percentage = self.builder.get_object("mining_percentage")
        self.mining_progress_bar = self.builder.get_object("mining_progress_bar") 


        # Show the window
        self.win.connect("destroy", self.on_window_destroy)
        self.win.present()

    def on_window_destroy(self, widget):
        # Quit the application when the window is closed
        self.quit()


    def switch_to_mining_stack_page(self):
        """Switch to the mining page in the GtkStack."""
        #self.stack_switcher.set_active(1)  
        self.stack.set_visible_child(self.mining_page_box)

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
        button.set_sensitive(False)

    def start_mining(self):
        minero = Minero()
        miner_thread = threading.Thread(target=minero.mine)
        miner_thread.start()
        while(miner_thread.is_alive and not minero.isMining_finished):
            if(minero.isExtracting):
                self.update_mining_label("Extracting...")
            elif(minero.isMining):
                self.update_mining_label("Mining data...")
            self.update_mining_percentage(minero.mining_progress)
            self.update_mining_progress_bar(minero.mining_progress)
            time.sleep(0.5)
        self.update_mining_label("Finished!")
        self.songs = minero.rolas
        miner_thread.join()  # This will block until the thread has finished
        self.populate_song_list()


    def populate_song_list(self):
        
        for song in self.songs:       
            # Add the song instance to the song_liststore
            self.song_liststore.append(song)
        
