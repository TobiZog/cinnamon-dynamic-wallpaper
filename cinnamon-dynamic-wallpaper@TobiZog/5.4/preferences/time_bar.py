import math

def create_bar(image_width, image_height, times):
  image_code = ['<svg xmlns="http://www.w3.org/2000/svg" width="' + str(image_width) + '" height="210">']
  colors = ["00193dff", "05597fff", "54babfff", "bfe3c2ff", "ffbf6bff", "fdb55cff", "f37f73ff", "7f3d85ff", "4a217aff", "00193dff"]

  for i in range(0, 10):
    start_point = (((100 / 1440) * times[i] / 100) * image_width)
    width = math.ceil((((100 / 1440) * (times[i + 1] - times[i]) / 100) * image_width))
    image_code.append('<rect fill="#%s" x="%s" y="60" width="%s" height="100"/>' % (colors[i], start_point, width))

    bar_part_mid = start_point + width / 2

    if (i < 5):
      polyline_x = i * 10 + 10
      polyline_y = 0
      image_x = 100 + i * (200 + 8)
    elif (i < 9):
      polyline_x = (i - 4) * 10 + 160
      polyline_y = 210
      image_x = 200 + (i - 5) * (200 + 8)
    
    if i < 9:
      image_code.append(
          '<polyline points="%s,%s %s,%s %s,%s %s,100" stroke="#%s" fill="none" stroke-width="5" />' % 
          (image_x, polyline_y, image_x, polyline_x, bar_part_mid, polyline_x, bar_part_mid, colors[i])
          )
      
  for i in range(0, 8):
    image_code.append(
      '<line x1="%s" y1="60" x2="%s" y2="160" stroke="gray" stroke-width="2" />' %
        (i * (image_width // 8), i * (image_width // 8))
      )
    
    image_code.append(
      '<text x="%s" y="155" fill="gray" font-size="20" font-family="Liberation Sans">%s</text>' %
        (i * (image_width // 8) + 5, i * 3)
    )

  # Write to file
  file = open("time_bar.svg", "w")
  for i in image_code:
    file.write(i + '\n')

  file.write('</svg>')