import urllib.request, json

class Location():
  def __init__(self):
    self.GEO_URL = "https://get.geojs.io/v1/ip/geo.json"

  def run(self) -> dict:
    request = urllib.request.urlopen(self.GEO_URL)

    data = json.load(request)

    return {
      "latitude": data["latitude"],
      "longitude": data["longitude"]
    }
