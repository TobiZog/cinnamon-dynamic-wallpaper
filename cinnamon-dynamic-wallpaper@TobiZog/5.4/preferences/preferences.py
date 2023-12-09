#!/usr/bin/python3

# Imports
import gi, os
from time_bar import create_bar

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf


# Global definitions
GLADE_URI = os.path.dirname(os.path.abspath(__file__)) + "/preferences.glade"


class Preferences:
	""" Preference window class
	"""
	def __init__(self) -> None:
		self.builder = Gtk.Builder()
		self.builder.add_from_file(GLADE_URI)
		self.builder.connect_signals(self)

		# Time bar
		# todo: Sample times
		create_bar(1036, 200, [0, 455, 494, 523, 673, 792, 882, 941, 973, 1013, 1440])
		pixbuf = GdkPixbuf.Pixbuf.new_from_file("time_bar.svg")
		self.builder.get_object("img_bar").set_from_pixbuf(pixbuf)


	def show(self):
		""" Display the window to the screen
		"""
		window = self.builder.get_object("window_main")
		window.show_all()

		self.builder.get_object("lbr_heic").set_visible(False)
		self.builder.get_object("lbr_folder").set_visible(False)

		Gtk.main()

	
	def onDestroy(self, *args):
		""" Lifecycle handler when window will be destroyed
		"""
		Gtk.main_quit()


if __name__ == "__main__":
	Preferences().show()