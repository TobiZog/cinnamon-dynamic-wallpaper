import os, json
from pathlib import Path

from service.display import *
from service.cinnamon_pref_handler import *
from service.suntimes import *
from service.time_bar_chart import *
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
		self.network_location_provider = ["geojs.io", "ip-api.com"]

		# Objects from scripts
		self.screen_height = Display().get_screen_height()
		self.cinnamon_prefs = Cinnamon_Pref_Handler()
		self.time_bar_chart = Time_Bar_Chart()
		self.suntimes = Suntimes()

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
				pass
				# todo self.suntimes.calc_suntimes(float(self.ui.etr_latitude.get_text()), float(self.ui.etr_longitude.get_text()))	

			
			# Get all time periods. Store the minutes to the list and print the values to the text views
			for i in range(0, 10):
				time_range_now = self.suntimes.day_periods[i]

				if i != 9:
					time_range_next = self.suntimes.day_periods[i + 1]
				else:
					time_range_next = time(hour=23, minute=59)

				# todo self.ui.etr_periods[i].set_text(
				# 	str(time_range_now.hour).rjust(2, '0') + ":" + str(time_range_now.minute).rjust(2, '0') + \
				# 		" - " + str(time_range_next.hour).rjust(2, '0') + ":" + str(time_range_next.minute).rjust(2, '0'))
				
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

		
