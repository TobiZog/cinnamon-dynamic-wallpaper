#!/usr/bin/python3

# Imports
import gi, os, subprocess
from scripts.time_bar_chart import Time_Bar_Chart
from scripts.cinnamon_pref_handler import *
from scripts.suntimes import *
from scripts.location import *
from enums.PreferenceEnums import PrefenceEnums
from enums.ImageSourceEnum import ImageSourceEnum
from enums.PeriodSourceEnum import PeriodSourceEnum

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf


# Global definitions
PREFERENCES_URI = os.path.dirname(os.path.abspath(__file__))
GLADE_URI = PREFERENCES_URI + "/preferences.glade"




class Preferences:
	""" Preference window class
	"""

	#################### Lifecycle ####################

	def __init__(self) -> None:
		self.builder = Gtk.Builder()
		self.builder.add_from_file(GLADE_URI)
		self.builder.connect_signals(self)

		self.time_bar_chart = Time_Bar_Chart()
		self.c_prefs = Cinnamon_Pref_Handler()

		# Suntimes object
		self.suntimes = Suntimes(float(self.c_prefs.prefs[PrefenceEnums.LATITUDE_AUTO]), 
													 float(self.c_prefs.prefs[PrefenceEnums.LONGITUDE_AUTO]))


		########## UI objects ##########
		
		## Image Configuration
		self.tb_image_set = self.builder.get_object("tb_image_set")
		self.tb_heic_file = self.builder.get_object("tb_heic_file")
		self.tb_source_folder = self.builder.get_object("tb_source_folder")
		self.lbr_image_set = self.builder.get_object("lbr_image_set")
		self.lbr_heic_file = self.builder.get_object("lbr_heic_file")
		self.lbr_source_folder = self.builder.get_object("lbr_source_folder")
		self.img_bar = self.builder.get_object("img_bar")
		self.sw_expand_over_all_displays = self.builder.get_object("sw_expand_over_all_displays")
		self.sw_show_on_lock_screen = self.builder.get_object("sw_show_on_lock_screen")
		self.etr_periods = [
			self.builder.get_object("etr_period_1"), self.builder.get_object("etr_period_2"),
			self.builder.get_object("etr_period_3"), self.builder.get_object("etr_period_4"),
			self.builder.get_object("etr_period_5"), self.builder.get_object("etr_period_6"),
			self.builder.get_object("etr_period_7"), self.builder.get_object("etr_period_8"),
			self.builder.get_object("etr_period_9"), self.builder.get_object("etr_period_10"),
		]

		## Location & Times
		self.tb_network_location = self.builder.get_object("tb_network_location")
		self.lb_current_location = self.builder.get_object("lb_current_location")
		self.lbr_current_location = self.builder.get_object("lbr_current_location")
		self.tb_custom_location = self.builder.get_object("tb_custom_location")
		self.tb_time_periods = self.builder.get_object("tb_time_periods")
		self.lbr_network_location = self.builder.get_object("lbr_network_location")
		self.spb_network_location_refresh_time = self.builder.get_object("spb_network_location_refresh_time")
		self.lbr_custom_location_longitude = self.builder.get_object("lbr_custom_location_longitude")
		self.lbr_custom_location_latitude = self.builder.get_object("lbr_custom_location_latitude")
		self.lbr_time_periods = self.builder.get_object("lbr_time_periods")
		self.etr_longitude = self.builder.get_object("etr_longitude")
		self.etr_latitude = self.builder.get_object("etr_latitude")


	def show(self):
		""" Display the window to the screen
		"""
		window = self.builder.get_object("window_main")
		window.show_all()


		# Load from preferences
		if self.c_prefs.prefs[PrefenceEnums.IMAGE_SOURCE] == ImageSourceEnum.IMAGESET:
			self.tb_image_set.set_active(True)
		elif self.c_prefs.prefs[PrefenceEnums.IMAGE_SOURCE] == ImageSourceEnum.HEICFILE:
			self.tb_heic_file.set_active(True)
		elif self.c_prefs.prefs[PrefenceEnums.IMAGE_SOURCE] == ImageSourceEnum.SOURCEFOLDER:
			self.tb_source_folder.set_active(True)

		self.sw_expand_over_all_displays.set_active(self.c_prefs.prefs[PrefenceEnums.EXPAND_OVER_ALL_DISPLAY])
		self.sw_show_on_lock_screen.set_active(self.c_prefs.prefs[PrefenceEnums.SHOW_ON_LOCK_SCREEN])


		if self.c_prefs.prefs[PrefenceEnums.PERIOD_SOURCE] == PeriodSourceEnum.NETWORKLOCATION:
			self.tb_network_location.set_active(True)
		elif self.c_prefs.prefs[PrefenceEnums.PERIOD_SOURCE] == PeriodSourceEnum.CUSTOMLOCATION:
			self.tb_custom_location.set_active(True)
		elif self.c_prefs.prefs[PrefenceEnums.PERIOD_SOURCE] == PeriodSourceEnum.CUSTOMTIMEPERIODS:
			self.tb_time_periods.set_active(True)



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
		self.time_bar_chart.create_bar_chart(PREFERENCES_URI, 1200, 150, time_periods_min)

		# Load to the view
		pixbuf = GdkPixbuf.Pixbuf.new_from_file(PREFERENCES_URI + "/time_bar.svg")
		self.img_bar.set_from_pixbuf(pixbuf)


		# Show the main window
		Gtk.main()

	
	def on_destroy(self, *args):
		""" Lifecycle handler when window will be destroyed
		"""
		Gtk.main_quit()


	#################### Callbacks ####################
		
	## Image Configuration
		
	def on_toggle_button_image_set_clicked(self, button):
		if button.get_active():
			self.c_prefs.prefs[PrefenceEnums.IMAGE_SOURCE] = ImageSourceEnum.IMAGESET
			self.tb_heic_file.set_active(False)
			self.tb_source_folder.set_active(False)

			self.lbr_image_set.set_visible(True)
			self.lbr_heic_file.set_visible(False)
			self.lbr_source_folder.set_visible(False)
		
	def on_toggle_button_heic_file_clicked(self, button):
		if button.get_active():
			self.c_prefs.prefs[PrefenceEnums.IMAGE_SOURCE] = ImageSourceEnum.HEICFILE
			self.tb_image_set.set_active(False)
			self.tb_source_folder.set_active(False)

			self.lbr_image_set.set_visible(False)
			self.lbr_heic_file.set_visible(True)
			self.lbr_source_folder.set_visible(False)

	def on_toggle_button_source_folder_clicked(self, button):
		if button.get_active():
			self.c_prefs.prefs[PrefenceEnums.IMAGE_SOURCE] = ImageSourceEnum.SOURCEFOLDER
			self.tb_image_set.set_active(False)
			self.tb_heic_file.set_active(False)

			self.lbr_image_set.set_visible(False)
			self.lbr_heic_file.set_visible(False)
			self.lbr_source_folder.set_visible(True)
	

	## Location & Times

	def on_toggle_button_network_location_clicked(self, button):
		if button.get_active():
			self.c_prefs.prefs[PrefenceEnums.PERIOD_SOURCE] = PeriodSourceEnum.NETWORKLOCATION
			self.tb_custom_location.set_active(False)
			self.tb_time_periods.set_active(False)

			self.lbr_network_location.set_visible(True)
			self.lbr_current_location.set_visible(True)
			self.lbr_custom_location_longitude.set_visible(False)
			self.lbr_custom_location_latitude.set_visible(False)
			self.lbr_time_periods.set_visible(False)

			self.spb_network_location_refresh_time.set_value(self.c_prefs.prefs[PrefenceEnums.LOCATION_REFRESH_INTERVALS])
		

			# Start a thread to get the current location
			locationThread = Location()
			locationThread.start()
			locationThread.join()

			location = locationThread.result

			# Display the location in the UI
			self.lb_current_location.set_text("Latitude: " + location["latitude"] + \
																		 ", Longitude: " + location["longitude"])
			
			# Store the location to the preferences
			self.c_prefs.prefs[PrefenceEnums.LATITUDE_AUTO] = float(location["latitude"])
			self.c_prefs.prefs[PrefenceEnums.LONGITUDE_AUTO] = float(location["longitude"])


	def on_toggle_button_custom_location_clicked(self, button):
		if button.get_active():
			self.c_prefs.prefs[PrefenceEnums.PERIOD_SOURCE] = PeriodSourceEnum.CUSTOMLOCATION
			self.tb_network_location.set_active(False)
			self.tb_time_periods.set_active(False)

			self.lbr_network_location.set_visible(False)
			self.lbr_current_location.set_visible(False)
			self.lbr_custom_location_longitude.set_visible(True)
			self.lbr_custom_location_latitude.set_visible(True)
			self.lbr_time_periods.set_visible(False)

			self.etr_latitude.set_text(str(self.c_prefs.prefs[PrefenceEnums.LATITUDE_CUSTOM]))
			self.etr_longitude.set_text(str(self.c_prefs.prefs[PrefenceEnums.LONGITUDE_CUSTOM]))


	def on_toggle_button_time_periods_clicked(self, button):
		if button.get_active():
			self.c_prefs.prefs[PrefenceEnums.PERIOD_SOURCE] = PeriodSourceEnum.CUSTOMTIMEPERIODS
			self.tb_network_location.set_active(False)
			self.tb_custom_location.set_active(False)

			self.lbr_network_location.set_visible(False)
			self.lbr_current_location.set_visible(False)
			self.lbr_custom_location_longitude.set_visible(False)
			self.lbr_custom_location_latitude.set_visible(False)
			self.lbr_time_periods.set_visible(True)


	def on_spb_network_location_refresh_time_changed(self, spin_button):
		self.c_prefs.prefs[PrefenceEnums.LOCATION_REFRESH_INTERVALS] = spin_button.get_value()


	def on_etr_longitude_changed(self, entry):
		try:
			self.c_prefs.prefs[PrefenceEnums.LONGITUDE_CUSTOM] = float(entry.get_text())
		except:
			pass


	def on_etr_latitude_changed(self, entry):
		try:
			self.c_prefs.prefs[PrefenceEnums.LATITUDE_CUSTOM] = float(entry.get_text())
		except:
			pass


	# About

	def on_cinnamon_spices_website_button_clicked(self, button):
		subprocess.Popen(["xdg-open", "https://cinnamon-spices.linuxmint.com/extensions/view/97"])

	def on_github_website_button_clicked(self, button):
		subprocess.Popen(["xdg-open", "https://github.com/TobiZog/cinnamon-dynamic-wallpaper"])

	def on_create_issue_button_clicked(self, button):
		subprocess.Popen(["xdg-open", "https://github.com/TobiZog/cinnamon-dynamic-wallpaper/issues/new"])


	def on_apply(self, *args):
			# Store all values to the JSON file
			self.c_prefs.store_preferences()

			# Close the window
			self.on_destroy()


if __name__ == "__main__":
	Preferences().show()