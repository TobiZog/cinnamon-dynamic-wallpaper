import os, json
from enums.PreferenceEnums import PrefenceEnums

# Location of the Cinnamon preference file since Cinnamon 5.4
pref_location = os.path.expanduser("~") + \
  "/.config/cinnamon/spices/cinnamon-dynamic-wallpaper@TobiZog/cinnamon-dynamic-wallpaper@TobiZog.json"


def write_to_preferences(parameter: PrefenceEnums, value: str):
  """ Write a preference value to the JSON file

  Args:
      parameter (PrefenceEnums): Name of the parameter
      value (str): Value to write
  """
  with open(pref_location, "r") as pref_file:
    pref_data = json.load(pref_file)

  if parameter in pref_data:
    pref_data[parameter]["value"] = value
  else:
    pref_data[parameter] = {
      "type": "entry",
      "default": "",
      "description": "",
      "value": value
    }

  with open(pref_location, "w") as pref_file:
    json.dump(pref_data, pref_file, separators=(',', ':'), indent=4)


def read_str_from_preferences(parameter: PrefenceEnums) -> str:
  """ Read a value from the JSON file

  Args:
      parameter (PrefenceEnums): Name of the parameter to get

  Returns:
      str: Value of the parameter
  """
  try:
    with open(pref_location, "r") as pref_file:
      pref_data = json.load(pref_file)
  except:
    return ""

  if parameter in pref_data:
    return pref_data[parameter]["value"]
  else:
    return ""
  
def read_int_from_preferences(parameter: PrefenceEnums) -> int:
  value = read_str_from_preferences(parameter)

  if value == "":
    return 0
  else:
    return int(value)
  
def read_float_from_preferences(parameter: PrefenceEnums) -> float:
  value = read_str_from_preferences(parameter)

  if value == "":
    return 0.0
  else:
    return float(value)