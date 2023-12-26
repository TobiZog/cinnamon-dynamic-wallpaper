import urllib.request, json
from threading import Thread

class Location(Thread):
  def __init__(self):
    Thread.__init__(self)
    self.GEO_URL = "https://get.geojs.io/v1/ip/geo.json"

  def run(self) -> dict:
    request = urllib.request.urlopen(self.GEO_URL)

    data = json.load(request)

    self.result = {
      "latitude": data["latitude"],
      "longitude": data["longitude"]
    }
