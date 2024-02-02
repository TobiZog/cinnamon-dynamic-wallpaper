import urllib.request, json
from enums.NetworkLocationProvider import NetworkLocationProvider

class Location():
  """ Class to handle location requests
  """
  def __init__(self):
    pass

  def get_location(self, provider: NetworkLocationProvider) -> dict:
    """ Request the location via network

    Returns:
        dict: latitude and longitude
    """
    request = urllib.request.urlopen(provider.value)

    data = json.load(request)

    if provider == NetworkLocationProvider.GEOJS:
      return {
        "latitude": data["latitude"],
        "longitude": data["longitude"]
      }
    elif provider == NetworkLocationProvider.IPAPI:
      return {
        "latitude": data["lat"],
        "longitude": data["lon"]
      }
