#!/usr/bin/python3

############################################################
#                         Imports                          #
############################################################

# Packages
import gi, os, subprocess, time
from datetime import timedelta

# Local scripts
from scripts import cinnamon_pref_handler, dialogs, display, images, location, suntimes, time_bar_chart, ui
from loop import *
from enums.ImageSourceEnum import ImageSourceEnum
from enums.PeriodSourceEnum import PeriodSourceEnum
from enums.NetworkLocationProvider import NetworkLocationProvider

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf






class Preferences:
	""" Preference window class
	"""

	############################################################
	#                         Lifecycle                        #
	############################################################

	def __init__(self) -> None:
		# UI helper object
		self.ui = ui.UI(self.builder)

		# Layout breakpoint for smaller displays
		self.smaller_ui_height = 1000


	def show(self):
		""" Display the window to the screen
		"""
		self.ui.show_main_window(self.builder, self.smaller_ui_height, self.prefs)

		# Time diagram
		try:
			self.refresh_chart()
		except:
			self.dialogs.message_dialog("Error on creating time bar!")

	


if __name__ == "__main__":
	Preferences().show()