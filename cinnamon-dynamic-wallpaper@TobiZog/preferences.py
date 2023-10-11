#!/usr/bin/python3

import gi, os, math, cairo

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

GLADE_URI = os.path.dirname(os.path.abspath(__file__)) + "/prefs.glade"

class Preferences:
	def __init__(self) -> None:
		self.builder = Gtk.Builder()
		self.builder.add_from_file(GLADE_URI)
		self.builder.connect_signals(self)

		# 0:00 = 0%
		# 7:05 = 29.58
		# 7:39 = 32.08
		# 8:20 = 34.58
		# 11:46 = 49.17
		# 14:32 = 60.42
		# 16:36 = 69.17
		# 17:57 = 74.58
		# 18:41 = 77.92
		# 19:15 = 80

		# Numbers for test purposes
		self.create_doughnut([29.57, 2.51, 2.5, 14.6, 11.26, 8.76, 5.42, 3.35, 2.09])

		
		pixbuf = GdkPixbuf.Pixbuf.new_from_file("example.svg")
		self.builder.get_object("image").set_from_pixbuf(pixbuf)


	def create_doughnut(self, list_of_percentages: list):
		color_list = [
			[0.00, 0.10, 0.24],
			[0.02, 0.35, 0.50],
			[0.33, 0.73, 0.75],
			[0.75, 0.89, 0.76],
			[1.00, 0.75, 0.42],
			[0.99, 0.71, 0.36],
			[0.95, 0.50, 0.45],
			[0.50, 0.24, 0.52],
			[0.29, 0.13, 0.48],
			[0.00, 0.10, 0.24],
			]
		
		image_height = 350
		image_width = 350
		

		with cairo.SVGSurface("example.svg", image_height, image_width) as surface:
			# Create the draw object
			context = cairo.Context(surface)

			# Calculate sizes
			xc, yc = image_height / 2, image_width / 2
			radius = image_height * 0.35
			doughnut_width = image_height * 0.2

			# -25 turns the graph 45° anti-clockwise
			total_percentage = -25

			# Completes the doughnut to 100%
			list_of_percentages.append(100 - sum(list_of_percentages))


			context.set_line_width(doughnut_width)

			# Draw the arc parts
			for i, percentage in enumerate(list_of_percentages):
				print(i)
				context.set_source_rgb(color_list[i][0], color_list[i][1], color_list[i][2])

				if total_percentage != 0:
					angle1 = 360 / (100 / total_percentage) * (math.pi/180)
				else:
					angle1 = 0
				
				angle2 = 360 / (100 / (total_percentage + percentage)) * (math.pi/180)

				context.arc(xc, yc, radius, angle1, angle2)
				total_percentage += percentage
				context.stroke()

			# Draw the times labels
			context.set_source_rgb(0.5, 0.5, 0.5)
			# context.set_font_size(18)

			# context.move_to(xc - 20, 20)
			# context.show_text("00")

			# context.move_to(360, yc)
			# context.show_text("06")

			# context.move_to(xc - 20, image_height)
			# context.show_text("12")

			# context.move_to(10, yc)
			# context.show_text("18")
			# context.stroke()

			# Draw the hour strokes
			context.set_line_width(2)
			lines_list = [
				[[xc, yc - radius + doughnut_width / 2 - 5], [xc, yc - radius + doughnut_width / 2 + 5]], 
				[[xc + radius - doughnut_width / 2 - 5, yc], [xc + radius - doughnut_width / 2 + 5, yc]], 
				[[xc, yc + radius - doughnut_width / 2 - 5], [xc, yc + radius - doughnut_width / 2 + 5]],
				[[xc - radius + doughnut_width / 2 - 5, yc], [xc - radius + doughnut_width / 2 + 5, yc]], 
				]

			for line in lines_list:
				context.move_to(line[0][0], line[0][1])
				context.line_to(line[1][0], line[1][1])
				context.stroke()



	def show(self):
		window = self.builder.get_object("window_main")
		window.show_all()

		Gtk.main()

	
	def onDestroy(self, *args):
		Gtk.main_quit()

if __name__ == "__main__":
	Preferences().show()