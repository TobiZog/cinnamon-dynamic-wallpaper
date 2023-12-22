#!/usr/bin/python3

# Imports
import gi, os, subprocess
from scripts.time_bar import create_bar_chart
from scripts.cinnamon_pref_handler import *
from scripts.suntimes import *
from enums.PreferenceEnums import PrefenceEnums
from enums.ImageSourceEnum import ImageSourceEnum
from enums.PeriodSourceEnum import PeriodSourceEnum

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

		self.suntimes = Suntimes(48.1663, 11.5683)


		########## UI objects ##########
		
		## Image Configuration
		self.tbImageSet = self.builder.get_object("tb_image_set")
		self.tbHeicFile = self.builder.get_object("tb_heic_file")
		self.tbSourceFolder = self.builder.get_object("tb_source_folder")
		self.lbrImageSet = self.builder.get_object("lbr_image_set")
		self.lbrHeicFile = self.builder.get_object("lbr_heic_file")
		self.lbrSourceFolder = self.builder.get_object("lbr_source_folder")
		self.imgBar = self.builder.get_object("img_bar")
		self.swExpandOverAllDisplays = self.builder.get_object("sw_expand_over_all_displays")
		self.swShowOnLockScreen = self.builder.get_object("sw_show_on_lock_screen")
		self.etr_periods = [
			self.builder.get_object("etr_period_1"), self.builder.get_object("etr_period_2"),
			self.builder.get_object("etr_period_3"), self.builder.get_object("etr_period_4"),
			self.builder.get_object("etr_period_5"), self.builder.get_object("etr_period_6"),
			self.builder.get_object("etr_period_7"), self.builder.get_object("etr_period_8"),
			self.builder.get_object("etr_period_9"), self.builder.get_object("etr_period_10"),
		]

		## Location & Times
		self.tbNetworkLocation = self.builder.get_object("tb_network_location")
		self.tbCustomLocation = self.builder.get_object("tb_custom_location")
		self.tbTimePeriods = self.builder.get_object("tb_time_periods")
		self.lbrNetworkLocation = self.builder.get_object("lbr_network_location")
		self.spbNetworkLocationRefreshTime = self.builder.get_object("spb_network_location_refresh_time")
		self.lbrCustomLocationLongitude = self.builder.get_object("lbr_custom_location_longitude")
		self.lbrCustomLocationLatitude = self.builder.get_object("lbr_custom_location_latitude")
		self.lbrTimePeriods = self.builder.get_object("lbr_time_periods")
		self.etrLongitude = self.builder.get_object("etr_longitude")
		self.etrLatitude = self.builder.get_object("etr_latitude")


	def show(self):
		""" Display the window to the screen
		"""
		window = self.builder.get_object("window_main")
		window.show_all()


		# Load from preferences
		if read_str_from_preferences(PrefenceEnums.IMAGESOURCE) == ImageSourceEnum.IMAGESET:
			self.tbImageSet.set_active(True)
		elif read_str_from_preferences(PrefenceEnums.IMAGESOURCE) == ImageSourceEnum.HEICFILE:
			self.tbHeicFile.set_active(True)
		elif read_str_from_preferences(PrefenceEnums.IMAGESOURCE) == ImageSourceEnum.SOURCEFOLDER:
			self.tbSourceFolder.set_active(True)

		self.swExpandOverAllDisplays.set_active(read_str_from_preferences(PrefenceEnums.EXPANDOVERALLDISPLAY))
		self.swShowOnLockScreen.set_active(read_str_from_preferences(PrefenceEnums.SHOWONLOCKSCREEN))


		if read_str_from_preferences(PrefenceEnums.PERIODSOURCE) == PeriodSourceEnum.NETWORKLOCATION:
			self.tbNetworkLocation.set_active(True)
		elif read_str_from_preferences(PrefenceEnums.PERIODSOURCE) == PeriodSourceEnum.CUSTOMLOCATION:
			self.tbCustomLocation.set_active(True)
		elif read_str_from_preferences(PrefenceEnums.PERIODSOURCE) == PeriodSourceEnum.CUSTOMTIMEPERIODS:
			self.tbTimePeriods.set_active(True)

		self.spbNetworkLocationRefreshTime.set_value(read_int_from_preferences(PrefenceEnums.LOCATIONREFRESHINTERVALS))
		self.etrLatitude.set_text(read_str_from_preferences(PrefenceEnums.LATITUDE))
		self.etrLongitude.set_text(read_str_from_preferences(PrefenceEnums.LONGITUDE))


		########## Time diagram ##########

		# Stores the start times of the periods in minutes since midnight
		time_periods_min = []

		# Get all time periods. Store the minutes to the list and print the values to the text views
		for i in range(0, 10):
			time_range = self.suntimes.get_time_period(i)
			self.etr_periods[i].set_text(str(time_range[0].hour).rjust(2, '0') + ":" + str(time_range[0].minute).rjust(2, '0') +\
																 " - " + str(time_range[1].hour).rjust(2, '0') + ":" + str(time_range[1].minute).rjust(2, '0'))
			
			time_periods_min.append(time_range[0].hour * 60 + time_range[0].minute)
		
		# Create time bar
		create_bar_chart(1200, 150, time_periods_min)

		# Load to the view
		pixbuf = GdkPixbuf.Pixbuf.new_from_file("time_bar.svg")
		self.imgBar.set_from_pixbuf(pixbuf)


		# Show the main window
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


	# About

	def onCinnamonSpicesWebsiteButtonClicked(self, button):
		subprocess.Popen(["xdg-open", "https://cinnamon-spices.linuxmint.com/extensions/view/97"])

	def onGithubWebsiteButtonClicked(self, button):
		subprocess.Popen(["xdg-open", "https://github.com/TobiZog/cinnamon-dynamic-wallpaper"])

	def onCreateIssueButtonClicked(self, button):
		subprocess.Popen(["xdg-open", "https://github.com/TobiZog/cinnamon-dynamic-wallpaper/issues/new"])


	def onApply(self, *args):
			# todo: Store all values to settings
			if self.tbImageSet.get_active():
				write_to_preferences(PrefenceEnums.IMAGESOURCE, ImageSourceEnum.IMAGESET)
			elif self.tbHeicFile.get_active():
				write_to_preferences(PrefenceEnums.IMAGESOURCE, ImageSourceEnum.HEICFILE)
			elif self.tbSourceFolder.get_active():
				write_to_preferences(PrefenceEnums.IMAGESOURCE, ImageSourceEnum.SOURCEFOLDER)

			write_to_preferences(PrefenceEnums.EXPANDOVERALLDISPLAY, self.swExpandOverAllDisplays.get_active())
			write_to_preferences(PrefenceEnums.SHOWONLOCKSCREEN, self.swShowOnLockScreen.get_active())


			write_to_preferences(PrefenceEnums.LOCATIONREFRESHINTERVALS, self.spbNetworkLocationRefreshTime.get_value())
			write_to_preferences(PrefenceEnums.LATITUDE, self.etrLatitude.get_text())
			write_to_preferences(PrefenceEnums.LONGITUDE, self.etrLongitude.get_text())

			if self.tbNetworkLocation.get_active():
				write_to_preferences(PrefenceEnums.PERIODSOURCE, PeriodSourceEnum.NETWORKLOCATION)
			elif self.tbCustomLocation.get_active():
				write_to_preferences(PrefenceEnums.PERIODSOURCE, PeriodSourceEnum.CUSTOMLOCATION)
			elif self.tbTimePeriods.get_active():
				write_to_preferences(PrefenceEnums.PERIODSOURCE, PeriodSourceEnum.CUSTOMTIMEPERIODS)


			self.onDestroy()


if __name__ == "__main__":
	Preferences().show()