#!/usr/bin/python3

# Imports
import gi, os
from time_bar import create_bar_chart

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf


# Global definitions
GLADE_URI = os.path.dirname(os.path.abspath(__file__)) + "/preferences.glade"


class Preferences:
	""" Preference window class
	"""

	#################### Lifecycle ####################

	def __init__(self) -> None:
		self.builder = Gtk.Builder()
		self.builder.add_from_file(GLADE_URI)
		self.builder.connect_signals(self)


		# UI objects
		self.buttonImageSet = self.builder.get_object("tb_image")
		self.buttonHeicFile = self.builder.get_object("tb_heic")
		self.buttonSourceFolder = self.builder.get_object("tb_folder")
		self.listBoxRowImageSet = self.builder.get_object("lbr_image")
		self.listBoxRowHeicFile = self.builder.get_object("lbr_heic")
		self.listBoxRowSourceFolder = self.builder.get_object("lbr_folder")
		self.imgBar = self.builder.get_object("img_bar")


		# Time bar
		# todo: Sample times
		create_bar_chart(1036, 150, [0, 455, 494, 523, 673, 792, 882, 941, 973, 1013])
		pixbuf = GdkPixbuf.Pixbuf.new_from_file("time_bar.svg")
		self.imgBar.set_from_pixbuf(pixbuf)


	def show(self):
		""" Display the window to the screen
		"""
		window = self.builder.get_object("window_main")
		window.show_all()

		self.buttonImageSet.set_active(True)

		Gtk.main()

	
	def onDestroy(self, *args):
		""" Lifecycle handler when window will be destroyed
		"""
		Gtk.main_quit()


	#################### Callbacks ####################

	def onToggleButtonImageClicked(self, button):
		if button.get_active():
			self.buttonHeicFile.set_active(False)
			self.buttonSourceFolder.set_active(False)

			self.listBoxRowImageSet.set_visible(True)
			self.listBoxRowHeicFile.set_visible(False)
			self.listBoxRowSourceFolder.set_visible(False)

	def onToggleButtonHeicClicked(self, button):
		if button.get_active():
			self.buttonImageSet.set_active(False)
			self.buttonSourceFolder.set_active(False)

			self.listBoxRowImageSet.set_visible(False)
			self.listBoxRowHeicFile.set_visible(True)
			self.listBoxRowSourceFolder.set_visible(False)

	def onToggleButtonFolderClicked(self, button):
		if button.get_active():
			self.buttonImageSet.set_active(False)
			self.buttonHeicFile.set_active(False)

			self.listBoxRowImageSet.set_visible(False)
			self.listBoxRowHeicFile.set_visible(False)
			self.listBoxRowSourceFolder.set_visible(True)



if __name__ == "__main__":
	Preferences().show()