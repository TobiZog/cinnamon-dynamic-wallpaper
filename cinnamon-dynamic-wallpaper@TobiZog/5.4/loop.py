#!/usr/bin/python3

from scripts.cinnamon_pref_handler import *
from scripts.suntimes import *
from datetime import datetime, time
from enums.PeriodSourceEnum import *
from scripts.location import *
from gi.repository import Gio
from PIL import Image


suntimes = Suntimes()
location_thread = Location()

background_settings = Gio.Settings.new("org.cinnamon.desktop.background")

class Loop():
  def __init__(self) -> None:
    self.prefs = Cinnamon_Pref_Handler()

    # Position should estimate by network
    if self.prefs.period_source == PeriodSourceEnum.NETWORKLOCATION:
      location_thread.start()
      location_thread.join()

      location = location_thread.result

      suntimes.calc_suntimes(float(location["latitude"]), float(location["longitude"]))
      self.start_times = suntimes.day_periods

    # Position is given by user
    elif self.prefs.prefs[PrefenceEnums.PERIOD_SOURCE] == PeriodSourceEnum.CUSTOMLOCATION:
      suntimes.calc_suntimes(float(self.prefs.latitude_custom), float(self.prefs.longitude_custom))
      self.start_times = suntimes.day_periods

    # No position, concrete times
    else:
      def string_to_time_converter(raw_str: str) -> time:
        hour = raw_str[0:raw_str.find(":")]
        minute = raw_str[raw_str.find(":") + 1:]

        return time(hour=int(hour), minute=int(minute))
      
      self.start_times = [
        string_to_time_converter(self.prefs.period_custom_start_time[0]),
        string_to_time_converter(self.prefs.period_custom_start_time[1]),
        string_to_time_converter(self.prefs.period_custom_start_time[2]),
        string_to_time_converter(self.prefs.period_custom_start_time[3]),
        string_to_time_converter(self.prefs.period_custom_start_time[4]),
        string_to_time_converter(self.prefs.period_custom_start_time[5]),
        string_to_time_converter(self.prefs.period_custom_start_time[6]),
        string_to_time_converter(self.prefs.period_custom_start_time[7]),
        string_to_time_converter(self.prefs.period_custom_start_time[8]),
        string_to_time_converter(self.prefs.period_custom_start_time[9])
      ]


  def exchange_image(self):
    """ Replace the desktop image
    """
    # Get the time of day
    time_now = time(datetime.now().hour, datetime.now().minute)

    # Assign the last image as fallback
    self.current_image_uri = self.prefs.source_folder + self.prefs.period_images[9]

    for i in range(0, 9):
      # Replace the image URI, if it's not the last time period of the day
      if self.start_times[i] <= time_now and time_now < self.start_times[i + 1]:
        self.current_image_uri = self.prefs.source_folder + self.prefs.period_images[i]
        break
    
    # Set the background
    background_settings['picture-uri'] = "file://" + self.current_image_uri

    # Set background stretching
    background_settings['picture-options'] = self.prefs.picture_aspect

    if self.prefs.dynamic_background_color:
      self.set_background_gradient()

    
  def set_background_gradient(self):
    """ Setting a gradient background to hide images, which are not high enough
    """
    # Load the image
    im = Image.open(self.current_image_uri)
    pix = im.load()

    # Width and height of the current setted image
    width, height = im.size

    # Color of the top and bottom pixel in the middle of the image
    top_color = pix[width / 2,0]
    bottom_color = pix[width / 2, height - 1]

    # Create the gradient
    background_settings['color-shading-type'] = "vertical"
    background_settings['primary-color'] = f"#{top_color[0]:x}{top_color[1]:x}{top_color[2]:x}"
    background_settings['secondary-color'] = f"#{bottom_color[0]:x}{bottom_color[1]:x}{bottom_color[2]:x}"


# Needed for JavaScript
if __name__ == "__main__":
  l = Loop()
  l.exchange_image()