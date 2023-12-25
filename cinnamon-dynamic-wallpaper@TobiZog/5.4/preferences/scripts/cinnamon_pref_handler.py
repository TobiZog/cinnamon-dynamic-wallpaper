import os, json
from enums.PreferenceEnums import PrefenceEnums

class Cinnamon_Pref_Handler:
  def __init__(self) -> None:
    # Location of the Cinnamon preference file since Cinnamon 5.4
    self.pref_location = os.path.expanduser("~") + \
      "/.config/cinnamon/spices/cinnamon-dynamic-wallpaper@TobiZog/cinnamon-dynamic-wallpaper@TobiZog.json"


  def write_to_preferences(self, parameter: PrefenceEnums, value: str):
    """ Write a preference value to the JSON file

    Args:
        parameter (PrefenceEnums): Name of the parameter
        value (str): Value to write
    """
    with open(self.pref_location, "r") as pref_file:
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

    with open(self.pref_location, "w") as pref_file:
      json.dump(pref_data, pref_file, separators=(',', ':'), indent=4)


  def read_str_from_preferences(self, parameter: PrefenceEnums) -> str:
    """ Read a value from the JSON file

    Args:
        parameter (PrefenceEnums): Name of the parameter to get

    Returns:
        str: Value of the parameter
    """
    try:
      with open(self.pref_location, "r") as pref_file:
        pref_data = json.load(pref_file)
    except:
      return ""

    if parameter in pref_data:
      return pref_data[parameter]["value"]
    else:
      return ""
    

  def read_int_from_preferences(self, parameter: PrefenceEnums) -> int:
    """ Read a value from the JSON file

    Args:
        parameter (PrefenceEnums): Name of the parameter to get

    Returns:
        str: Value of the parameter
    """
    value = self.read_str_from_preferences(parameter)

    if value == "":
      return 0
    else:
      return int(value)
    

  def read_float_from_preferences(self, parameter: PrefenceEnums) -> float:
    """ Read a value from the JSON file

    Args:
        parameter (PrefenceEnums): Name of the parameter to get

    Returns:
        str: Value of the parameter
    """
    value = self.read_str_from_preferences(parameter)

    if value == "":
      return 0.0
    else:
      return float(value)