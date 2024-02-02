import os, json
from PIL import Image
from gi.repository import Gio

from service.display import *
from service.cinnamon_pref_handler import *
from service.suntimes import *
from service.time_bar_chart import *
from service.location import *
from enums.PeriodSourceEnum import *

class Main_View_Model:
	def __init__(self) -> None:
		# Paths
		self.WORKING_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
		self.RES_DIR = self.WORKING_DIR + "/res"
		self.IMAGES_DIR = self.RES_DIR + "/images"
		self.GLADE_URI = self.RES_DIR + "/preferences.glade"
		self.TIMEBAR_URI = self.WORKING_DIR + "/src/time_bar.svg"
		self.TIMEBAR_URI_POLYLINES = self.WORKING_DIR + "/src/time_bar_polylines.svg"
		self.PREF_URI = os.path.expanduser("~") + \
      "/.config/cinnamon/spices/cinnamon-dynamic-wallpaper@TobiZog/cinnamon-dynamic-wallpaper@TobiZog.json"

		# Datasets
		self.image_sets = ["aurora", "beach", "bitday", "cliffs", "earth", "gradient", "lakeside", "mountains", "sahara"]
		self.picture_aspects = ["centered", "scaled", "stretched", "zoom", "spanned"]
		self.network_location_provider = ["geojs.io", "ip-api.com", "ipwho.is"]

		# Objects from scripts
		self.screen_height = Display().get_screen_height()
		self.cinnamon_prefs = Cinnamon_Pref_Handler()
		self.time_bar_chart = Time_Bar_Chart()
		self.suntimes = Suntimes()
		self.location = Location()

		self.background_settings = Gio.Settings.new("org.cinnamon.desktop.background")

		# Breakpoint for smaller UI
		self.breakpoint_ui = 1000


	def refresh_charts(self):
		# Stores the start times of the periods in minutes since midnight
		time_periods_min = []

		if self.cinnamon_prefs.period_source == PeriodSourceEnum.CUSTOMTIMEPERIODS:
			for i in range(0, 10):
				time_str = self.cinnamon_prefs.period_custom_start_time[i]

				time_periods_min.append(int(time_str[0:2]) * 60 + int(time_str[3:5]))
		else:
			if self.cinnamon_prefs.period_source == PeriodSourceEnum.NETWORKLOCATION:
				self.suntimes.calc_suntimes(float(self.cinnamon_prefs.latitude_auto), float(self.cinnamon_prefs.longitude_auto))
			else:
				self.suntimes.calc_suntimes(float(self.cinnamon_prefs.latitude_custom), float(self.cinnamon_prefs.longitude_custom))	

			
			# Get all time periods. Store the minutes to the list and print the values to the text views
			for i in range(0, 10):
				time_range_now = self.suntimes.day_periods[i]
				time_periods_min.append(time_range_now.hour * 60 + time_range_now.minute)


		# Create time bar
		# Reduce size for small displays
		if self.screen_height < self.breakpoint_ui:
			bar_width = 1150
			bar_height = 110
		else:
			bar_width = 1300
			bar_height = 150

		self.time_bar_chart.create_bar_chart_with_polylines(self.TIMEBAR_URI_POLYLINES, bar_width, bar_height, time_periods_min)
		self.time_bar_chart.create_bar_chart(self.TIMEBAR_URI, bar_width, bar_height, time_periods_min)

	
	def refresh_location(self) -> bool:
		""" Updating the location by IP, store the result to cinnamon_prefs

		Returns:
				bool: Successful or not
		"""
		current_location = self.location.get_location(self.cinnamon_prefs.network_location_provider)

		if current_location['success']:
			self.cinnamon_prefs.latitude_auto = current_location['latitude']
			self.cinnamon_prefs.longitude_auto = current_location['longitude']

		return current_location['success']
	

	def string_to_time_converter(raw_str: str) -> time:
		""" Convert a time string like "12:34" to a time object

		Args:
				raw_str (str): Raw string

		Returns:
				time: Time object
		"""
		hour = raw_str[0:raw_str.find(":")]
		minute = raw_str[raw_str.find(":") + 1:]

		return time(hour=int(hour), minute=int(minute))


	def calulate_time_periods(self) -> list:
		if self.cinnamon_prefs.period_source == PeriodSourceEnum.CUSTOMTIMEPERIODS:
			# User uses custom time periods
			return [
				self.string_to_time_converter(self.cinnamon_prefs.period_custom_start_time[0]),
        self.string_to_time_converter(self.cinnamon_prefs.period_custom_start_time[1]),
        self.string_to_time_converter(self.cinnamon_prefs.period_custom_start_time[2]),
        self.string_to_time_converter(self.cinnamon_prefs.period_custom_start_time[3]),
        self.string_to_time_converter(self.cinnamon_prefs.period_custom_start_time[4]),
        self.string_to_time_converter(self.cinnamon_prefs.period_custom_start_time[5]),
        self.string_to_time_converter(self.cinnamon_prefs.period_custom_start_time[6]),
        self.string_to_time_converter(self.cinnamon_prefs.period_custom_start_time[7]),
        self.string_to_time_converter(self.cinnamon_prefs.period_custom_start_time[8]),
        self.string_to_time_converter(self.cinnamon_prefs.period_custom_start_time[9])
			]
		else:
			# Time periods have to be estimate by coordinates
			if self.cinnamon_prefs.period_source == PeriodSourceEnum.NETWORKLOCATION:
				# Get coordinates from the network
				self.refresh_location()
				self.suntimes.calc_suntimes(self.cinnamon_prefs.latitude_auto, self.cinnamon_prefs.longitude_auto)

			elif self.cinnamon_prefs.period_source == PeriodSourceEnum.CUSTOMLOCATION:
				# Get coordinates from user input
				self.suntimes.calc_suntimes(self.cinnamon_prefs.latitude_custom, self.cinnamon_prefs.longitude_custom)

			# Return the time periods
			return self.suntimes.day_periods


	def refresh_image(self):
		""" Replace the desktop image if needed
		"""
		start_times = self.calulate_time_periods()

		# Get the time of day
		time_now = time(datetime.now().hour, datetime.now().minute)

		# Assign the last image as fallback
		self.current_image_uri = self.cinnamon_prefs.source_folder + self.cinnamon_prefs.period_images[9]

		for i in range(0, 9):
			# Replace the image URI, if it's not the last time period of the day
			if start_times[i] <= time_now and time_now < start_times[i + 1]:
				self.current_image_uri = self.cinnamon_prefs.source_folder + self.cinnamon_prefs.period_images[i]
			break

		# Set the background
		self.background_settings['picture-uri'] = "file://" + self.current_image_uri

		# Set background stretching
		self.background_settings['picture-options'] = self.cinnamon_prefs.picture_aspect


	def set_background_gradient(self):
		""" Setting a gradient background to hide images, which are not high enough
		"""
		# Load the image
		try:
			im = Image.open(self.current_image_uri)
			pix = im.load()

			# Width and height of the current setted image
			width, height = im.size

			# Color of the top and bottom pixel in the middle of the image
			top_color = pix[width / 2,0]
			bottom_color = pix[width / 2, height - 1]

			# Create the gradient
			self.background_settings['color-shading-type'] = "vertical"

			if self.cinnamon_prefs.dynamic_background_color:
				self.background_settings['primary-color'] = f"#{top_color[0]:x}{top_color[1]:x}{top_color[2]:x}"
				self.background_settings['secondary-color'] = f"#{bottom_color[0]:x}{bottom_color[1]:x}{bottom_color[2]:x}"
			else:
				self.background_settings['primary-color'] = "#000000"
				self.background_settings['secondary-color'] = "#000000"
		except:
			self.background_settings['primary-color'] = "#000000"
			self.background_settings['secondary-color'] = "#000000"
