from math import pi, sin, asin, acos, cos
from datetime import datetime, timedelta

# Constants
DAY_MS = 1000 * 60 * 60 * 24
YEAR_1970 = 2440588

# Julian date of 01.01.2000 11:59 UTC
YEAR_2000 = 2451545


class Suntimes:
  def __init__(self, latitude: float, longitude: float) -> None:
    """ Initialization

    Args:
        latitude (float): Latitude of the position
        longitude (float): Longitude of the position
    """
    self.latitude = latitude
    self.longitude = longitude
    self.date = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000
    self.sun_events_of_day()


  def from_julian(self, j_date: float) -> datetime:
    """ Convert Julian date to a datetime

    Args:
        j_date (float): Julian date

    Returns:
        datetime: Converted datetime object
    """
    j_date = (j_date + 0.5 - YEAR_1970) * DAY_MS
    return datetime.fromtimestamp(j_date / 1000)


  def sun_events_of_day(self):
    """ Calculate all values to estimate the day periods
    """
    rad = pi / 180
    lw = rad * (-self.longitude)

    d = (self.date / DAY_MS) - 0.5 + YEAR_1970 - YEAR_2000
    n = round(d - 0.0009 - lw / (2 * pi))
    ds = 0.0009 + lw / (2 * pi) + n

    self.M = rad * (357.5291 + 0.98560028 * ds)
    C = rad * (1.9148 * sin(self.M) + 0.02 * sin(2 * self.M) + 0.0003 * sin(3 * self.M))
    P = rad * 102.9372
    self.L = self.M + C + P + pi

    dec = asin(sin(rad * 23.4397) * sin(self.L))
    self.j_noon = YEAR_2000 + ds + 0.0053 * sin(self.M) - 0.0069 * sin(2 * self.L)

    # -8 = Start of Civil dawn/dusk
    # -2 = Start of Sunrise/Sunset
    # 0 = Start/End of daylight phases
    self.angles = [-10, -4, 0]

    for i in range(0, len(self.angles)):
      self.angles[i] = rad * self.angles[i]
      self.angles[i] = acos((sin(self.angles[i]) - sin(rad * self.latitude) * sin(dec)) / 
                            (cos(rad * self.latitude) * cos(dec)))
      self.angles[i] = 0.0009 + (self.angles[i] + lw) / (2 * pi) + n


  def angle_correction(self, angle: float) -> float:
    """ Last correction for the sun angle

    Args:
        angle (float): Angle before the correction

    Returns:
        float: Angle after the correction
    """
    return YEAR_2000 + angle + 0.0053 * sin(self.M) - 0.0069 * sin(2 * self.L)


  def get_time_period(self, period_nr: int) -> list:
    """ Get start and end time of a time period

    Args:
        period_nr (int):  Number between 0 and 9
                          0 = Early Night
                          1 = Civial dawn
                          2 = Sunrise
                          3 = Morning
                          4 = Noon
                          5 = Afternoon
                          6 = Evening
                          7 = Sunset
                          8 = Civial Dusk
                          9 = Late Night

    Returns:
        list: Two datetime objects
    """
    # Early night
    if period_nr == 0:
      res = [datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
             self.from_julian(2 * self.j_noon - self.angle_correction(self.angles[0])) - timedelta(minutes=1)]
    
    # Civilian dawn, Sunrise
    elif period_nr <= 2:
      res = [self.from_julian(2 * self.j_noon - self.angle_correction(self.angles[period_nr - 1])),
             self.from_julian(2 * self.j_noon - self.angle_correction(self.angles[period_nr])) - timedelta(minutes=1)]
  
    # Morning, Noon, Afternoon, Evening
    elif period_nr <= 6:
      daylength = self.get_time_period(8)[0] - self.get_time_period(2)[1]

      res = [self.get_time_period(2)[1] + ((daylength / 4) * (period_nr - 3)), 
             self.get_time_period(2)[1] + ((daylength / 4) * (period_nr - 2))]
      
    # Sunset, Civial dusk
    elif period_nr <= 8:
      res = [self.from_julian(self.angle_correction(self.angles[9 - period_nr])),
             self.from_julian(self.angle_correction(self.angles[8 - period_nr])) - timedelta(minutes=1)]
    
    # Late Night
    elif period_nr == 9:
      res = [self.from_julian(YEAR_2000 + self.angles[0] + 0.0053 * sin(self.M) - 0.0069 * sin(2 * self.L)),
             datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)]
    
    return res
