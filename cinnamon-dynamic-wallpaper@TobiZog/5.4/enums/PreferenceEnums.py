from enum import Enum

class PrefenceEnums(enumerate):
  PICTURE_ASPECT = "picture_aspect"
  DYNAMIC_BACKGROUND_COLOR = "dynamic_background_color"

  # Which type of image source will be used
  # image_set, heic_file, source_folder
  IMAGE_SOURCE = "image_source"

  SELECTED_IMAGE_SET = "selected_image_set"
  SOURCE_FOLDER = "source_folder"

  PERIOD_0_IMAGE = "period_0_image"
  PERIOD_1_IMAGE = "period_1_image"
  PERIOD_2_IMAGE = "period_2_image"
  PERIOD_3_IMAGE = "period_3_image"
  PERIOD_4_IMAGE = "period_4_image"
  PERIOD_5_IMAGE = "period_5_image"
  PERIOD_6_IMAGE = "period_6_image"
  PERIOD_7_IMAGE = "period_7_image"
  PERIOD_8_IMAGE = "period_8_image"
  PERIOD_9_IMAGE = "period_9_image"


  # How the period will estimage
  # network_location, custom_location, custom_time_periods
  PERIOD_SOURCE = "period_source"

  LOCATION_REFRESH_INTERVALS = "location_refresh_intervals"
  LATITUDE_AUTO = "latitude_auto"
  LONGITUDE_AUTO = "longitude_auto"
  LATITUDE_CUSTOM = "latitude_custom"
  LONGITUDE_CUSTOM = "longitude_custom"

  PERIOD_0_STARTTIME = "period_0_custom_start_time"
  PERIOD_1_STARTTIME = "period_1_custom_start_time"
  PERIOD_2_STARTTIME = "period_2_custom_start_time"
  PERIOD_3_STARTTIME = "period_3_custom_start_time"
  PERIOD_4_STARTTIME = "period_4_custom_start_time"
  PERIOD_5_STARTTIME = "period_5_custom_start_time"
  PERIOD_6_STARTTIME = "period_6_custom_start_time"
  PERIOD_7_STARTTIME = "period_7_custom_start_time"
  PERIOD_8_STARTTIME = "period_8_custom_start_time"
  PERIOD_9_STARTTIME = "period_9_custom_start_time"
