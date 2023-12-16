import math

image_code = []

colors = [
    "00193dff", 
    "05597fff", 
    "54babfff", 
    "bfe3c2ff", 
    "ffbf6bff", 
    "fdb55cff", 
    "f37f73ff", 
    "7f3d85ff", 
    "4a217aff", 
    "00193dff"
  ]

bar_pos_x = []

def create_bar_chart(image_width, image_height, times):
  create_bar(image_width, image_height, times)
  create_polylines(image_width, image_height)
  create_time_markers(image_width, image_height)

  # Write to file
  image_code.insert(0, '<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s">' % (image_width, image_height))
  image_code.append('</svg>')
  
  file = open("time_bar.svg", "w")
  for i in image_code:
    file.write(i + '\n')


def create_bar(image_width: int, image_height: int, times: list):
  """ Generates the code for the horizontal multi-color bar chart

  Args:
      image_width (int): Total width of the image
      image_height (int): Total height of the image
      times (list): List of start times of the periods, in minutes
  """
  x = 0
  y = 40
  width = 0
  height = image_height - 80
  times.append(1440)

  # Adding the bar parts
  for i in range(1, len(times)):
    width = math.ceil((((100 / 1440) * (times[i] - times[i - 1]) / 100) * image_width))

    image_code.append(
      '<rect fill="#%s" x="%s" y="%s" width="%s" height="%s"/>' % (colors[i - 1], x, y, width, height)
    )

    bar_pos_x.append(x)
    x += width


def create_time_markers(image_width: int, image_height: int):
  """ Generates the code for the vertical hour markers

  Args:
      image_width (int): Total width of the image
      image_height (int): Total height of the image
  """
  for i in range(0, 8):
    image_code.append(
      '<line x1="%s" y1="40" x2="%s" y2="%s" stroke="gray" stroke-width="2" />' %
        (i * (image_width // 8), i * (image_width // 8), image_height - 40)
    )
    
    image_code.append(
      '<text x="%s" y="%s" fill="gray" font-size="20" font-family="Liberation Sans">%s</text>' %
        (i * (image_width // 8) + 5, image_height - 45, i * 3)
    )


def create_polylines(image_width: int, image_height: int):
  """ Generates the code for the polylines which connect the images with the bar sections

  Args:
      image_width (int): Total width of the image
      image_height (int): Total height of the image
  """
  bar_x_start = 0

  bar_pos_x.append(image_width)
  
  for i in range(0, len(bar_pos_x) - 1):
    # X-Middle of a bar
    bar_mid = bar_x_start + (bar_pos_x[i + 1] - bar_x_start) / 2

    # Position of the image in the window
    image_x = (image_width - 32) / 10 + ((i // 2) % 5) * image_width / 5
  
    # i == 0, 2, 4, ... => Upper Polylines
    if (i % 2 == 0):
      polyline_y = 0
    else:
      polyline_y = image_height

    if i == 0 or i == 8:
      polyline_x = 30
    elif i == 2 or i == 6:
      polyline_x = 20
    elif i == 1 or i == 9:
      polyline_x = image_height - 30
    elif i == 3 or i == 7:
      polyline_x = image_height - 20
    elif i == 5:
      polyline_x = image_height - 10
    else:
      polyline_x = 10
    
    image_code.append(
      '<polyline points="%s,%s %s,%s %s,%s %s,%s" stroke="#%s" fill="none" stroke-width="5" />' % 
        (image_x, polyline_y, image_x, polyline_x, bar_mid, polyline_x, bar_mid, image_height / 2, colors[i])
    )

    # Store the end point of the bar as start point of the next
    bar_x_start = bar_pos_x[i + 1]

# Hannover
#create_bar_chart(1036, 180, [0, 455, 494, 523, 673, 792, 882, 941, 973, 1013])

# Other Test bar
#create_bar_chart(1036, 180, [0, 180, 190, 523, 673, 792, 882, 941, 973, 1300])