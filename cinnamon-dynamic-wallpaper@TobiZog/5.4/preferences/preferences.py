#!/usr/bin/python3

# Imports
import gi, os, subprocess
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


		########## UI objects ##########
		
		## Image Configuration
		self.tbImageSet = self.builder.get_object("tb_image_set")
		self.tbHeicFile = self.builder.get_object("tb_heic_file")
		self.tbSourceFolder = self.builder.get_object("tb_source_folder")
		self.lbrImageSet = self.builder.get_object("lbr_image_set")
		self.lbrHeicFile = self.builder.get_object("lbr_heic_file")
		self.lbrSourceFolder = self.builder.get_object("lbr_source_folder")
		self.imgBar = self.builder.get_object("img_bar")

		## Location & Times
		self.tbNetworkLocation = self.builder.get_object("tb_network_location")
		self.tbCustomLocation = self.builder.get_object("tb_custom_location")
		self.tbTimePeriods = self.builder.get_object("tb_time_periods")
		self.lbrNetworkLocation = self.builder.get_object("lbr_network_location")
		self.lbrCustomLocationLongitude = self.builder.get_object("lbr_custom_location_longitude")
		self.lbrCustomLocationLatitude = self.builder.get_object("lbr_custom_location_latitude")
		self.lbrTimePeriods = self.builder.get_object("lbr_time_periods")


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

		self.tbImageSet.set_active(True)
		self.tbNetworkLocation.set_active(True)

		Gtk.main()

	
	def onDestroy(self, *args):
		""" Lifecycle handler when window will be destroyed
		"""
		Gtk.main_quit()


	#################### Callbacks ####################
		
	## Image Configuration
		
	def onToggleButtonImageSetClicked(self, button):
		if button.get_active():
			self.tbHeicFile.set_active(False)
			self.tbSourceFolder.set_active(False)

			self.lbrImageSet.set_visible(True)
			self.lbrHeicFile.set_visible(False)
			self.lbrSourceFolder.set_visible(False)
		
	def onToggleButtonHeicFileClicked(self, button):
		if button.get_active():
			self.tbImageSet.set_active(False)
			self.tbSourceFolder.set_active(False)

			self.lbrImageSet.set_visible(False)
			self.lbrHeicFile.set_visible(True)
			self.lbrSourceFolder.set_visible(False)

	def onToggleButtonSourceFolderClicked(self, button):
		if button.get_active():
			self.tbImageSet.set_active(False)
			self.tbHeicFile.set_active(False)

			self.lbrImageSet.set_visible(False)
			self.lbrHeicFile.set_visible(False)
			self.lbrSourceFolder.set_visible(True)
	

	## Location & Times

	def onToggleButtonNetworkLocationClicked(self, button):
		if button.get_active():
			self.tbCustomLocation.set_active(False)
			self.tbTimePeriods.set_active(False)

			self.lbrNetworkLocation.set_visible(True)
			self.lbrCustomLocationLongitude.set_visible(False)
			self.lbrCustomLocationLatitude.set_visible(False)
			self.lbrTimePeriods.set_visible(False)

	def onToggleButtonCustomLocationClicked(self, button):
		if button.get_active():
			self.tbNetworkLocation.set_active(False)
			self.tbTimePeriods.set_active(False)

			self.lbrNetworkLocation.set_visible(False)
			self.lbrCustomLocationLongitude.set_visible(True)
			self.lbrCustomLocationLatitude.set_visible(True)
			self.lbrTimePeriods.set_visible(False)

	def onToggleButtonTimePeriodsClicked(self, button):
		if button.get_active():
			self.tbNetworkLocation.set_active(False)
			self.tbCustomLocation.set_active(False)

			self.lbrNetworkLocation.set_visible(False)
			self.lbrCustomLocationLongitude.set_visible(False)
			self.lbrCustomLocationLatitude.set_visible(False)
			self.lbrTimePeriods.set_visible(True)

	def onCinnamonSpicesWebsiteButtonClicked(self, button):
		subprocess.Popen(["xdg-open", "https://cinnamon-spices.linuxmint.com/extensions/view/97"])

	def onGithubWebsiteButtonClicked(self, button):
		subprocess.Popen(["xdg-open", "https://github.com/TobiZog/cinnamon-dynamic-wallpaper"])

	def onCreateIssueButtonClicked(self, button):
		subprocess.Popen(["xdg-open", "https://github.com/TobiZog/cinnamon-dynamic-wallpaper/issues/new"])



if __name__ == "__main__":
	Preferences().show()