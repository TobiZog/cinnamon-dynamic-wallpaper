#!/usr/bin/python3

from scripts.cinnamon_pref_handler import *
from scripts.suntimes import *
from datetime import datetime, time
from enums.PreferenceEnums import *
from enums.PeriodSourceEnum import *
from scripts.location import *
import gi
from gi.repository import Gio

prefs = Cinnamon_Pref_Handler()
suntimes = Suntimes()
location_thread = Location()

background_settings = Gio.Settings.new("org.cinnamon.desktop.background")

class Loop():
  def __init__(self) -> None:
    # Position should estimate by network
    if prefs.prefs[PrefenceEnums.PERIOD_SOURCE] == PeriodSourceEnum.NETWORKLOCATION:
      location_thread.start()
      location_thread.join()

      location = location_thread.result

      suntimes.calc_suntimes(float(location["latitude"]), float(location["longitude"]))
      self.start_times = suntimes.day_periods

    # Position is given by user
    elif prefs.prefs[PrefenceEnums.PERIOD_SOURCE] == PeriodSourceEnum.CUSTOMLOCATION:
      suntimes.calc_suntimes(float(prefs.prefs[PrefenceEnums.LATITUDE_CUSTOM]), float(prefs.prefs[PrefenceEnums.LONGITUDE_CUSTOM]))
      self.start_times = suntimes.day_periods

    # No position, concrete times
    else:
      def string_to_time_converter(raw_str: str) -> time:
        hour = raw_str[0:raw_str.find(":")]
        minute = raw_str[raw_str.find(":") + 1:]

        return time(hour=int(hour), minute=int(minute))
      
      self.start_times = [
        string_to_time_converter(prefs.prefs[PrefenceEnums.PERIOD_0_STARTTIME]),
        string_to_time_converter(prefs.prefs[PrefenceEnums.PERIOD_1_STARTTIME]),
        string_to_time_converter(prefs.prefs[PrefenceEnums.PERIOD_2_STARTTIME]),
        string_to_time_converter(prefs.prefs[PrefenceEnums.PERIOD_3_STARTTIME]),
        string_to_time_converter(prefs.prefs[PrefenceEnums.PERIOD_4_STARTTIME]),
        string_to_time_converter(prefs.prefs[PrefenceEnums.PERIOD_5_STARTTIME]),
        string_to_time_converter(prefs.prefs[PrefenceEnums.PERIOD_6_STARTTIME]),
        string_to_time_converter(prefs.prefs[PrefenceEnums.PERIOD_7_STARTTIME]),
        string_to_time_converter(prefs.prefs[PrefenceEnums.PERIOD_8_STARTTIME]),
        string_to_time_converter(prefs.prefs[PrefenceEnums.PERIOD_9_STARTTIME])
      ]


  def exchange_image(self):
    """ Replace the desktop image
    """
    time_now = time(datetime.now().hour, datetime.now().minute)
        
    for i in range(0, 9):
      if self.start_times[i] <= time_now and time_now < self.start_times[i + 1]:
        background_settings['picture-uri'] = "file://" + prefs.prefs[PrefenceEnums.SOURCE_FOLDER] + prefs.prefs["period_%d_image" % (i)]
        return

    background_settings['picture-uri'] = "file://" + prefs.prefs[PrefenceEnums.SOURCE_FOLDER] + prefs.prefs[PrefenceEnums.PERIOD_9_IMAGE]


if __name__ == "__main__":
  l = Loop()
  l.exchange_image()
