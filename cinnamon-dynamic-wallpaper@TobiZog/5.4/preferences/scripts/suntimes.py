# # import datetime, math

# # day_ms = 1000 * 60 * 60 * 24
# # year_1970 = 2440588
# # year_2000 = 2451545

# # def from_julian(j) -> datetime.date:
# #   return datetime.date(ms_date = (j + 0.5 - year_1970))

# # def sun_events_of_day(latitude, longitude, date):
# #   rad = math.pi / 180
# #   lw = rad * (-longitude)

# #   d = (date / day_ms) - 0.5 + year_1970 - year_2000
# #   n = math.floor(d - 0.0009 - lw / (2 * math.pi))
# #   ds = 0.0009 + lw / (2 * math.pi) + n

# #   M = rad * (357.5291 + 0.98560028 * ds)
# #   C = rad * (1.9148 * math.sin(M) + 0.02 * math.sin(2 * M) + 0.0003 * math.sin(3 * M))
# #   P = rad * 102.9372
# #   L = M + C + P + math.pi

# #   dec = math.asin(math.sin(rad * 23.4397) * math.sin(L))

# #   angles = [-0.833, -6]

# #   for angle in angles:
# #     angle *= rad
# #     angle = math.acos((math.sin(angle) - math.sin(rad * latitude) * math.sin(dec)) / (math.cos(rad * latitude) * math.cos(dec)))
# #     angle = 0.0009 + (angle + lw) / (2 * math.pi) + n

# #   j_noon = year_2000 + ds + 0.0053 * math.sin(M) - 0.0069 * math.sin(2 * L)

# #   print(from_julian(j_noon - (year_2000 + angles[1] + 0.0053 * math.sin(M) - 0.0069 * math.sin(2 * L) - j_noon)))


# # sun_events_of_day(48.1663, 11.5683, datetime.datetime.now())


# import datetime, math
# from math import cos, sin, acos, asin, tan
# from math import degrees as deg, radians as rad
# from datetime import date, datetime, time





# DAY_MS = 1000 * 60 * 60 * 24
# YEAR_1970 = 2440588
# YEAR_2000 = 2451545

# def date_to_julian(year, month, day):
#   if month <= 2:
#     year += 1
#     month += 12

#   A = math.trunc(year / 100.)
#   B = 2 - A + math.trunc(A / 4.)

#   if year < 0:
#     C = math.trunc((365.25 * year) - 0.75)
#   else:
#     C = math.trunc(365.25 * year)

#   D = math.trunc(30.6001 * (month + 1))

#   return B + C + D + day + 1720994.5


# latitude_rad = rad(latitude)


# n = date_to_julian(datetime.now().year, datetime.now().month, datetime.now().day) - YEAR_2000 + 0.0008
# jstar = n - deg(longitude) / 360

# M_deg = (357.5291 + 0.98560028 * jstar) % 360
# M = M_deg * math.pi / 180

# C = 1.9148 * sin(M) + 0.0200 * sin(2*M) + 0.003 * sin(3*M)

# lamda = math.fmod(M_deg + C + 180 + 102.9372, 360) * math.pi / 180

# Jtransit = 2451545.5 + jstar + 0.0053 * sin(M) - 0.0069 * sin(2 * lamda)

# earth_tilt_rad = rad(23.44)
# angle_delta = asin(sin(lamda) * sin(earth_tilt_rad))
# sun_disc_rad = rad(-0.83)

# os_omega = 


# print(date_to_julian(2023, 12, 12))

# #s = sun(lat=48.1663, long=11.5683)

from math import pi, sin, asin, acos, cos
from datetime import datetime, timedelta

DAY_MS = 1000 * 60 * 60 * 24
YEAR_1970 = 2440588
YEAR_2000 = 2451545

class Suntimes:
  def __init__(self, latitude, longitude) -> None:
    self.latitude = latitude
    self.longitude = longitude
    self.date = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000
    self.sun_events_of_day()

  def from_julian(self, j_date) -> datetime:
    j_date = (j_date + 0.5 - YEAR_1970) * DAY_MS
    return datetime.fromtimestamp(j_date / 1000)

  def sun_events_of_day(self):
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

  def angle_correction(self, angle: float) -> datetime:
    return (YEAR_2000 + angle + 0.0053 * sin(self.M) - 0.0069 * sin(2 * self.L))
  
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
    if period_nr == 0:
      res = [datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
             self.from_julian(2 * self.j_noon - self.angle_correction(self.angles[0])) - timedelta(minutes=1)]
    elif period_nr <= 2:
      res = [self.from_julian(2 * self.j_noon - self.angle_correction(self.angles[period_nr - 1])),
             self.from_julian(2 * self.j_noon - self.angle_correction(self.angles[period_nr])) - timedelta(minutes=1)]
    elif period_nr <= 6:
      daylength = self.get_time_period(8)[0] - self.get_time_period(2)[1]

      res = [self.get_time_period(2)[1] + ((daylength / 4) * (period_nr - 3)), 
             self.get_time_period(2)[1] + ((daylength / 4) * (period_nr - 2))]
    elif period_nr <= 8:
      res = [self.from_julian(self.angle_correction(self.angles[9 - period_nr])),
             self.from_julian(self.angle_correction(self.angles[8 - period_nr])) - timedelta(minutes=1)]
    elif period_nr == 9:
      res = [self.from_julian(YEAR_2000 + self.angles[0] + 0.0053 * sin(self.M) - 0.0069 * sin(2 * self.L)),
             datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)]
    
    return res
