import os, json

class Cinnamon_Pref_Handler:
  def __init__(self) -> None:
    # Location of the Cinnamon preference file since Cinnamon 5.4
    self.pref_location = os.path.expanduser("~") + \
      "/.config/cinnamon/spices/cinnamon-dynamic-wallpaper@TobiZog/cinnamon-dynamic-wallpaper@TobiZog.json"
    
    self.prefs = {}

    self.load_preferences()


  def load_preferences(self):
    with open(self.pref_location, "r") as pref_file:
      pref_data = json.load(pref_file)

    for i in pref_data:
      try:
        self.prefs[i] = pref_data[i]["value"]
      except:
        pass


  def store_preferences(self):
    with open(self.pref_location, "r") as pref_file:
      pref_data = json.load(pref_file)

    for i in pref_data:
      try:
        pref_data[i]["value"] = self.prefs[i]
      except:
        pass

    with open(self.pref_location, "w") as pref_file:
      json.dump(pref_data, pref_file, separators=(',', ':'), indent=4)
