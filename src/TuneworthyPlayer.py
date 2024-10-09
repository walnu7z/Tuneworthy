import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version('Gst', '1.0')
gi.require_version('Adw', '1')
from gi.repository import GLib, Gtk, Adw, GObject, Gst


class TuneworthyPlayer(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        # Load the UI from the .ui file
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./src/tuneworthy.ui")  # Adjust the path if necessary

        # Get the main window object from the UI file
        self.win = self.builder.get_object("window")  # Make sure the ID matches your UI file
        self.win.set_application(app)  # Set the application for the window

        # Show the window
        self.win.connect("destroy", self.on_window_destroy)
        self.win.present()

    def on_window_destroy(self, widget):
        # Quit the application when the window is closed
        self.quit()