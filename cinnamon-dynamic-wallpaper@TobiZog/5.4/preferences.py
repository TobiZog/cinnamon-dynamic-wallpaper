#!/usr/bin/python3

# Imports
import gi, os, subprocess, time
from datetime import timedelta
from scripts.time_bar_chart import Time_Bar_Chart
from scripts.cinnamon_pref_handler import *
from scripts.suntimes import *
from scripts.location import *
from scripts.images import *
from enums.PreferenceEnums import PrefenceEnums
from enums.ImageSourceEnum import ImageSourceEnum
from enums.PeriodSourceEnum import PeriodSourceEnum
from loop import *

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf


# Global definitions
PREFERENCES_URI = os.path.dirname(os.path.abspath(__file__))
GLADE_URI = PREFERENCES_URI + "/preferences.glade"


class Preferences:
	""" Preference window class
	"""

	############################################################
	#                         Lifecycle                        #
	############################################################

	def __init__(self) -> None:
		self.builder = Gtk.Builder()
		self.builder.add_from_file(GLADE_URI)
		self.builder.connect_signals(self)

		# Objects from external scripts
		self.time_bar_chart = Time_Bar_Chart()
		self.c_prefs = Cinnamon_Pref_Handler()
		self.suntimes = Suntimes()
		self.images = Images()
		
		########## UI objects ##########
		
		#### Page 1: Image Configuration
		self.tb_image_set = self.builder.get_object("tb_image_set")
		self.tb_heic_file = self.builder.get_object("tb_heic_file")
		self.tb_source_folder = self.builder.get_object("tb_source_folder")

		# Image set
		self.lbr_image_set = self.builder.get_object("lbr_image_set")
		self.cb_image_set = self.builder.get_object("cb_image_set")

		# HEIC file		
		self.lbr_heic_file = self.builder.get_object("lbr_heic_file")

		# Source folder
		self.lbr_source_folder = self.builder.get_object("lbr_source_folder")
		self.fc_source_folder = self.builder.get_object("fc_source_folder")

		# Time bar chart
		self.img_bar_images = self.builder.get_object("img_bar_images")
		self.etr_periods = [
			self.builder.get_object("etr_period_1"), self.builder.get_object("etr_period_2"),
			self.builder.get_object("etr_period_3"), self.builder.get_object("etr_period_4"),
			self.builder.get_object("etr_period_5"), self.builder.get_object("etr_period_6"),
			self.builder.get_object("etr_period_7"), self.builder.get_object("etr_period_8"),
			self.builder.get_object("etr_period_9"), self.builder.get_object("etr_period_10"),
		]

		self.img_periods = [
			self.builder.get_object("img_period_0"), self.builder.get_object("img_period_1"),
			self.builder.get_object("img_period_2"), self.builder.get_object("img_period_3"),
			self.builder.get_object("img_period_4"), self.builder.get_object("img_period_5"),
			self.builder.get_object("img_period_6"), self.builder.get_object("img_period_7"),
			self.builder.get_object("img_period_8"), self.builder.get_object("img_period_9"),
		]

		self.cb_periods = [
			self.builder.get_object("cb_period_0"), self.builder.get_object("cb_period_1"), 
			self.builder.get_object("cb_period_2"), self.builder.get_object("cb_period_3"), 
			self.builder.get_object("cb_period_4"), self.builder.get_object("cb_period_5"), 
			self.builder.get_object("cb_period_6"), self.builder.get_object("cb_period_7"), 
			self.builder.get_object("cb_period_8"), self.builder.get_object("cb_period_9"), 
		]



		#### Page 2: Location & Times
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


		# Page 3: Behaviour
		self.cb_picture_aspect: Gtk.ComboBox = self.builder.get_object("cb_picture_aspect")
		self.sw_dynamic_background_color: Gtk.Switch = self.builder.get_object("sw_dynamic_background_color")


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


		picture_aspects = ["mosaic", "centered", "scaled", "stretched", "zoom", "spanned"]
		self.add_items_to_combo_box(self.cb_picture_aspect, picture_aspects)
		self.set_active_combobox_item(self.cb_picture_aspect, self.c_prefs.prefs[PrefenceEnums.PICTURE_ASPECT])

		self.sw_dynamic_background_color.set_active(self.c_prefs.prefs[PrefenceEnums.DYNAMIC_BACKGROUND_COLOR])


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



	############################################################
	#												Local methods											 #
	############################################################

	def refresh_chart(self):
		""" Recomputes both time bar charts and load them to the UI
		"""
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


	def load_image_options_to_combo_boxes(self, options: list):
		""" Add a list of Strings to all image option comboboxes

		Args:
				options (list): All possible options
		"""
		for combobox in self.cb_periods:
			self.add_items_to_combo_box(combobox, options)


	def load_image_to_preview(self, image_preview: Gtk.Image, image_src: list):
		try:
			pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_src)
			pixbuf = pixbuf.scale_simple(250, 175, GdkPixbuf.InterpType.BILINEAR)

			image_preview.set_from_pixbuf(pixbuf)
		except:
			pass


	############################################################
	#										UI helper methods											 #
	############################################################

	def set_active_combobox_item(self, combobox: Gtk.ComboBoxText, active_item: str):
		""" Change active item in combobox by String value

		Args:
				combobox (Gtk.ComboBoxText): ComboBox to set active
				active_item (str): String item to set active
		"""
		list_store = combobox.get_model()

		for i in range(0, len(list_store)):
			row = list_store[i]
			if row[0] == active_item:
				combobox.set_active(i)


	def add_items_to_combo_box(self, combobox: Gtk.ComboBox, items: list):
		""" Add items to a combo box

		Args:
				combobox (Gtk.ComboBox): ComboBox where to add the options
				items (list): Possible options
		"""
		model = combobox.get_model()
		store = Gtk.ListStore(str)

		for image_set in items:
			store.append([image_set])

		combobox.set_model(store)

		if model == None:
			renderer_text = Gtk.CellRendererText()
			combobox.pack_start(renderer_text, True)
			combobox.add_attribute(renderer_text, "text", 0)



	############################################################
	#													Callbacks											 	 #
	############################################################

	## Image Configuration
			
	# +-----------+-----------+---------------+
	# | Image Set | HEIC file | Source Folder |
	# +-----------+-----------+---------------+

	def on_toggle_button_image_set_clicked(self, button: Gtk.Button):
		if button.get_active():
			self.c_prefs.prefs[PrefenceEnums.IMAGE_SOURCE] = ImageSourceEnum.IMAGESET
			self.tb_heic_file.set_active(False)
			self.tb_source_folder.set_active(False)

			self.lbr_image_set.set_visible(True)
			self.lbr_heic_file.set_visible(False)
			self.lbr_source_folder.set_visible(False)

			image_set_choices = ["aurora", "beach", "bitday", "cliffs", "gradient", "lakeside", "mountains", "sahara"]
			self.add_items_to_combo_box(self.cb_image_set, image_set_choices)

			self.set_active_combobox_item(self.cb_image_set, self.c_prefs.prefs[PrefenceEnums.SELECTED_IMAGE_SET])

			for i, combobox in enumerate(self.cb_periods):
				selected_image_name = self.c_prefs.prefs["period_%s_image" % (i)]
				self.set_active_combobox_item(combobox, selected_image_name)

			# Make the comboboxes invisible
			for combobox in self.cb_periods:
				combobox.set_visible(False)
		
	
	def on_toggle_button_heic_file_clicked(self, button: Gtk.Button):
		if button.get_active():
			self.c_prefs.prefs[PrefenceEnums.IMAGE_SOURCE] = ImageSourceEnum.HEICFILE
			self.tb_image_set.set_active(False)
			self.tb_source_folder.set_active(False)

			self.lbr_image_set.set_visible(False)
			self.lbr_heic_file.set_visible(True)
			self.lbr_source_folder.set_visible(False)

			# Make the comboboxes visible
			for combobox in self.cb_periods:
				combobox.set_visible(True)


	def on_toggle_button_source_folder_clicked(self, button: Gtk.Button):
		if button.get_active():
			self.c_prefs.prefs[PrefenceEnums.IMAGE_SOURCE] = ImageSourceEnum.SOURCEFOLDER
			self.tb_image_set.set_active(False)
			self.tb_heic_file.set_active(False)

			self.lbr_image_set.set_visible(False)
			self.lbr_heic_file.set_visible(False)
			self.lbr_source_folder.set_visible(True)

			# Make the comboboxes visible
			for combobox in self.cb_periods:
				combobox.set_visible(True)

			# Load the source folder to the view
			# This will update the comboboxes in the preview to contain the right items
			self.fc_source_folder.set_filename(self.c_prefs.prefs[PrefenceEnums.SOURCE_FOLDER])



	def on_cb_image_set_changed(self, combobox: Gtk.ComboBox):
		tree_iter = combobox.get_active_iter()

		if tree_iter is not None and self.c_prefs.prefs[PrefenceEnums.IMAGE_SOURCE] == ImageSourceEnum.IMAGESET:
			# Get the selected value
			model = combobox.get_model()
			selected_image_set = model[tree_iter][0]

			# Store to the preferences
			self.c_prefs.prefs[PrefenceEnums.SELECTED_IMAGE_SET] = selected_image_set
			self.c_prefs.prefs[PrefenceEnums.SOURCE_FOLDER] = os.path.abspath(os.path.join(PREFERENCES_URI, os.pardir)) + \
				  "/5.4/images/included_image_sets/" + selected_image_set + "/"
			
			# Load all possible options to the comboboxes
			image_names = self.images.get_images_from_folder(self.c_prefs.prefs[PrefenceEnums.SOURCE_FOLDER])
			self.load_image_options_to_combo_boxes(image_names)

			# Image sets have the same names for the images:
			# 9.jpg = Period 0
			# 1.jpg = Period 1
			# 2.jpg = Period 2
			# and so on....
			self.cb_periods[0].set_active(8)
			for i in range(1, 10):
				self.cb_periods[i].set_active(i - 1)


	def on_fc_heic_file_file_set(self, fc_button: Gtk.FileChooser):
		file_path = fc_button.get_filename()
		extract_folder = os.path.abspath(os.path.join(PREFERENCES_URI, os.pardir)) + \
				  "/images/extracted_images/"

		file_name = file_path[file_path.rfind("/") + 1:]
		file_name = file_name[:file_name.rfind(".")]

		# Update the preferences
		self.c_prefs.prefs[PrefenceEnums.SELECTED_IMAGE_SET] = ""
		self.c_prefs.prefs[PrefenceEnums.SOURCE_FOLDER] = extract_folder

		# Create the buffer folder
		try:
			os.mkdir(extract_folder)
		except:
			pass

		# Extract the HEIC file
		for file in self.images.get_images_from_folder(extract_folder):
			os.remove(extract_folder + file)

		os.system("heif-convert " + file_path + " " + extract_folder + file_name + ".jpg")

		# Collect all extracted images and push them to the comboboxes
		image_names = self.images.get_images_from_folder(self.c_prefs.prefs[PrefenceEnums.SOURCE_FOLDER])
		self.load_image_options_to_combo_boxes(image_names)

	

	def on_fc_source_folder_file_set(self, fc_button: Gtk.FileChooser):
		files = self.images.get_images_from_folder(fc_button.get_filename())

		# Update the preferences
		self.c_prefs.prefs[PrefenceEnums.SELECTED_IMAGE_SET] = ""
		self.c_prefs.prefs[PrefenceEnums.SOURCE_FOLDER] = fc_button.get_filename() + "/"
		
		if len(files) != 0:
			self.load_image_options_to_combo_boxes(files)

			# Load the values for the images from the preferences
			for i in range(0, 10):
				self.set_active_combobox_item(self.cb_periods[i], self.c_prefs.prefs["period_%s_image" % (i)])
		else:
			pass
	

	def on_cb_period_preview_changed(self, combobox: Gtk.ComboBox):
		tree_iter = combobox.get_active_iter()

		combobox_name = Gtk.Buildable.get_name(combobox)
		period_index = int(combobox_name[10:11])

		if tree_iter is not None:
			# Get the selected value
			model = combobox.get_model()
			image_file_name = model[tree_iter][0]

			# Store selection to preferences
			self.c_prefs.prefs["period_%s_image" % (period_index)] = image_file_name

			# Build up image path
			image_path = self.c_prefs.prefs[PrefenceEnums.SOURCE_FOLDER] + image_file_name

			self.load_image_to_preview(self.img_periods[period_index], image_path)
	

	## Location & Times

	def on_toggle_button_network_location_clicked(self, button: Gtk.Button):
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


	def on_toggle_button_custom_location_clicked(self, button: Gtk.Button):
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


	def on_toggle_button_time_periods_clicked(self, button: Gtk.Button):
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



	def on_spb_period_value_changed(self, spin_button: Gtk.SpinButton):
		""" Callback if one of the time spinners (minute or hour) will be clicked

					 (1)							 (2)							 (3)
			Previous period		Current period		 Next period
			12:34 - 14:40			14:41 - 16:20			16:21 - 17:30
													^
										Variable to change

		Args:
				spin_button (Gtk.SpinButton): SpinButton which was changed
		"""
		spin_button_name = Gtk.Buildable.get_name(spin_button)
		index = int(spin_button_name[11:12]) - 1

		# Determe time string and store to prefs
		time_current_start = datetime(2024,1,1, int(self.spb_periods_hour[index].get_value()), int(self.spb_periods_minute[index].get_value()))
		time_current_start_str = str(time_current_start.hour).rjust(2, '0') + ":" + str(time_current_start.minute).rjust(2, '0')

		self.c_prefs.prefs["period_%s_custom_start_time" % (index + 1)] = time_current_start_str
		

		time_previous_end = time_current_start - timedelta(minutes=1)
		self.lb_period_end[index].set_text(str(time_previous_end.hour).rjust(2, '0') + ":" + str(time_previous_end.minute).rjust(2, '0'))


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


	# Behaviour
		
	def on_cb_picture_aspect_changed(self, combobox: Gtk.ComboBox):
		tree_iter = combobox.get_active_iter()

		if tree_iter is not None:
			model = combobox.get_model()
			self.c_prefs.prefs[PrefenceEnums.PICTURE_ASPECT] = model[tree_iter][0]
			print(self.c_prefs.prefs[PrefenceEnums.PICTURE_ASPECT])
		
	def on_sw_dynamic_background_color_state_set(self, switch: Gtk.Switch, state):
		self.c_prefs.prefs[PrefenceEnums.DYNAMIC_BACKGROUND_COLOR] = state


	# About

	def on_cinnamon_spices_website_button_clicked(self, button: Gtk.Button):
		""" Callback for the button to navigate to the Cinnamon Spices web page of this project

		Args:
				button (Gtk.Button): Button which was clicked
		"""
		subprocess.Popen(["xdg-open", "https://cinnamon-spices.linuxmint.com/extensions/view/97"])


	def on_github_website_button_clicked(self, button: Gtk.Button):
		""" Callback for the button to navigate to the GitHub web page of this project

		Args:
				button (Gtk.Button): Button which was clicked
		"""
		subprocess.Popen(["xdg-open", "https://github.com/TobiZog/cinnamon-dynamic-wallpaper"])


	def on_create_issue_button_clicked(self, button):
		""" Callback for the button to navigate to the Issues page on GitHub of this project

		Args:
				button (Gtk.Button): Button which was clicked
		"""
		subprocess.Popen(["xdg-open", "https://github.com/TobiZog/cinnamon-dynamic-wallpaper/issues/new"])


	def on_apply(self, *args):
		""" Callback for the Apply button in the top bar
		"""
		# Store all values to the JSON file
		self.c_prefs.store_preferences()

		# Use the new settings
		loop = Loop()
		loop.exchange_image()

		# Close the window
		self.on_destroy()


if __name__ == "__main__":
	Preferences().show()