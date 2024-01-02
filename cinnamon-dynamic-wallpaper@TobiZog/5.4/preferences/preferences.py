#!/usr/bin/python3

# Imports
import gi, os, subprocess, time
from datetime import timedelta
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
		self.suntimes = Suntimes()
		
		########## UI objects ##########
		
		## Image Configuration
		self.tb_image_set = self.builder.get_object("tb_image_set")
		self.tb_heic_file = self.builder.get_object("tb_heic_file")
		self.tb_source_folder = self.builder.get_object("tb_source_folder")
		self.lbr_image_set = self.builder.get_object("lbr_image_set")
		self.lbr_heic_file = self.builder.get_object("lbr_heic_file")
		self.lbr_source_folder = self.builder.get_object("lbr_source_folder")
		self.img_bar_images = self.builder.get_object("img_bar_images")
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
		self.img_bar_times = self.builder.get_object("img_bar_times")
		self.spb_periods_hour = [
			self.builder.get_object("spb_period_1_hour"),
			self.builder.get_object("spb_period_2_hour"),
			self.builder.get_object("spb_period_3_hour"),
			self.builder.get_object("spb_period_4_hour"),
			self.builder.get_object("spb_period_5_hour"),
			self.builder.get_object("spb_period_6_hour"),
			self.builder.get_object("spb_period_7_hour"),
			self.builder.get_object("spb_period_8_hour"),
			self.builder.get_object("spb_period_9_hour"),
		]
		self.spb_periods_minute = [
			self.builder.get_object("spb_period_1_minute"),
			self.builder.get_object("spb_period_2_minute"),
			self.builder.get_object("spb_period_3_minute"),
			self.builder.get_object("spb_period_4_minute"),
			self.builder.get_object("spb_period_5_minute"),
			self.builder.get_object("spb_period_6_minute"),
			self.builder.get_object("spb_period_7_minute"),
			self.builder.get_object("spb_period_8_minute"),
			self.builder.get_object("spb_period_9_minute")
		]
		self.lb_period_end = [
			self.builder.get_object("lb_period_0_end"), self.builder.get_object("lb_period_1_end"),
			self.builder.get_object("lb_period_2_end"), self.builder.get_object("lb_period_3_end"),
			self.builder.get_object("lb_period_4_end"), self.builder.get_object("lb_period_5_end"),
			self.builder.get_object("lb_period_6_end"), self.builder.get_object("lb_period_7_end"),
			self.builder.get_object("lb_period_8_end"), self.builder.get_object("lb_period_9_end"), 
		]


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

		# Time diagram
		try:
			self.refresh_chart()
		except:
			pass

		# Show the main window
		Gtk.main()

	
	def on_destroy(self, *args):
		""" Lifecycle handler when window will be destroyed
		"""
		Gtk.main_quit()


	#################### Local methods ####################


	def refresh_chart(self):
		# Stores the start times of the periods in minutes since midnight
		time_periods_min = []

		if self.c_prefs.prefs[PrefenceEnums.PERIOD_SOURCE] == PeriodSourceEnum.CUSTOMTIMEPERIODS:
			for i in range(0, 10):
				time_str = self.c_prefs.prefs["period_%s_custom_start_time" % i]

				time_periods_min.append(int(time_str[0:2]) * 60 + int(time_str[3:5]))
		else:
			if self.c_prefs.prefs[PrefenceEnums.PERIOD_SOURCE] == PeriodSourceEnum.NETWORKLOCATION:
				self.suntimes.calc_suntimes(float(self.c_prefs.prefs[PrefenceEnums.LATITUDE_AUTO]), 
																float(self.c_prefs.prefs[PrefenceEnums.LONGITUDE_AUTO]))
			else:
				self.suntimes.calc_suntimes(float(self.etr_latitude.get_text()), float(self.etr_longitude.get_text()))	

			
			# Get all time periods. Store the minutes to the list and print the values to the text views
			for i in range(0, 10):
				time_range_now = self.suntimes.day_periods[i]

				if i != 9:
					time_range_next = self.suntimes.day_periods[i + 1]
				else:
					time_range_next = time(hour=23, minute=59)

				self.etr_periods[i].set_text(
					str(time_range_now.hour).rjust(2, '0') + ":" + str(time_range_now.minute).rjust(2, '0') +\
						" - " + str(time_range_next.hour).rjust(2, '0') + ":" + str(time_range_next.minute).rjust(2, '0'))
				
				time_periods_min.append(time_range_now.hour * 60 + time_range_now.minute)

		# Create time bar
		self.time_bar_chart.create_bar_chart_with_polylines(PREFERENCES_URI, 1200, 150, time_periods_min)
		self.time_bar_chart.create_bar_chart(PREFERENCES_URI, 1200, 150, time_periods_min)

		# Load to the views
		pixbuf = GdkPixbuf.Pixbuf.new_from_file(PREFERENCES_URI + "/time_bar_polylines.svg")
		self.img_bar_images.set_from_pixbuf(pixbuf)

		pixbuf2 = GdkPixbuf.Pixbuf.new_from_file(PREFERENCES_URI + "/time_bar.svg")
		self.img_bar_times.set_from_pixbuf(pixbuf2)


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

			self.refresh_chart()


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
			
			
			for i in range(0, 9):
				pref_value = self.c_prefs.prefs["period_%s_custom_start_time" % (i + 1)]
				time_parts = [int(pref_value[0:pref_value.find(":")]), int(pref_value[pref_value.find(":") + 1:])]

				self.spb_periods_hour[i].set_value(time_parts[0])
				self.spb_periods_minute[i].set_value(time_parts[1])



	def on_spb_period_value_changed(self, spin_button):
		""" Callback if one of the time spinners (minute or hour) will be clicked

					 (1)							 (2)							 (3)
			Previous period		Current period		 Next period
			12:34 - 14:40			14:41 - 16:20			16:21 - 17:30
													^
										Variable to change

		Args:
				spin_button (_type_): _description_
		"""
		spin_button_name = Gtk.Buildable.get_name(spin_button)
		index = int(spin_button_name[11:12]) - 1

		# Determe time string and store to prefs
		time_current_start = datetime(2024,1,1, int(self.spb_periods_hour[index].get_value()), int(self.spb_periods_minute[index].get_value()))
		time_current_start_str = str(time_current_start.hour).rjust(2, '0') + ":" + str(time_current_start.minute).rjust(2, '0')

		self.c_prefs.prefs["period_%s_custom_start_time" % (index + 1)] = time_current_start_str
		

		# (1) Update the start time of the previous period
		time_previous_end = time_current_start - timedelta(minutes=1)
		self.lb_period_end[index].set_text(str(time_previous_end.hour).rjust(2, '0') + ":" + str(time_previous_end.minute).rjust(2, '0'))

		# todo:
		# hours_next = self.spb_periods_hour[index + 1].get_value()
		# minutes_next = self.spb_periods_minute[index + 1].get_value()
		# time_next_start = datetime(2024, 1, 1, int(hours_next), int(minutes_next))

		# if time_next_start < time_current_start:
		# 	# (2) Update the end time of the current period
		# 	current_time_end = time_current_start + timedelta(minutes=1)
		# 	time_current_start_str = str(current_time_end.hour).rjust(2, '0') + ":" + str(current_time_end.minute).rjust(2, '0')


		self.refresh_chart()


	def on_spb_network_location_refresh_time_changed(self, spin_button):
		self.c_prefs.prefs[PrefenceEnums.LOCATION_REFRESH_INTERVALS] = spin_button.get_value()


	def on_etr_longitude_changed(self, entry):
		try:
			self.c_prefs.prefs[PrefenceEnums.LONGITUDE_CUSTOM] = float(entry.get_text())
			self.refresh_chart()
		except:
			pass


	def on_etr_latitude_changed(self, entry):
		try:
			self.c_prefs.prefs[PrefenceEnums.LATITUDE_CUSTOM] = float(entry.get_text())
			self.refresh_chart()
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