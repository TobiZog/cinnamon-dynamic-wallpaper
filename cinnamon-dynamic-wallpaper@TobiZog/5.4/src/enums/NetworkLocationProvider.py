from enum import Enum

class NetworkLocationProvider(Enum):
  GEOJS = "https://get.geojs.io/v1/ip/geo.json"
  IPAPI = "http://ip-api.com/json/?fields=61439"