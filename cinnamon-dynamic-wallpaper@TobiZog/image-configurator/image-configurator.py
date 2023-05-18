import gi, os, glob

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

DIR = os.path.dirname(os.path.abspath(__file__))
UI_FILE = DIR + "/image-configurator.glade"
EXPORT_DIR = "extracted"


class ImageConfigurator:
	def __init__(self) -> None:
		########### Class variables ###########



		try:
			os.mkdir(DIR + "/" + EXPORT_DIR)
		except:
			pass


		########### GTK stuff ###########
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		########### Glade Ressources ###########
		self.imageSetText = self.builder.get_object("lb_image_set")
		self.imageSetCb = self.builder.get_object("cb_image_set")

		self.fileChooserText = self.builder.get_object("lb_heic_file")
		self.fileChooserFc = self.builder.get_object("fc_heic_file")
		self.image_set_list_store = self.builder.get_object("image_set_list_store")
		self.ls_preview = self.builder.get_object("ls_preview")

		self.img_previews = [
			self.builder.get_object("img_preview_1"),
			self.builder.get_object("img_preview_2"),
			self.builder.get_object("img_preview_3"),
			self.builder.get_object("img_preview_4"),
			self.builder.get_object("img_preview_5"),
			self.builder.get_object("img_preview_6"),
			self.builder.get_object("img_preview_7"),
			self.builder.get_object("img_preview_8"),
			self.builder.get_object("img_preview_9")
		]

		self.cb_previews = [
			self.builder.get_object("cb_preview_1"),
			self.builder.get_object("cb_preview_2"),
			self.builder.get_object("cb_preview_3"),
			self.builder.get_object("cb_preview_4"),
			self.builder.get_object("cb_preview_5"),
			self.builder.get_object("cb_preview_6"),
			self.builder.get_object("cb_preview_7"),
			self.builder.get_object("cb_preview_8"),
			self.builder.get_object("cb_preview_9")
		]


		########### Load predefinitions and settings ###########
		self.image_set_list_store.append(["Big Sur Beach 2"])
		self.image_set_list_store.append(["Firewatch"])
		self.image_set_list_store.append(["Lakeside"])
		# todo


		try:
			# Create the combobox content
			self.createExtracted()
			self.changePreviewSpinners(self.extracted)

			# Load the images
			with open(DIR + "/selected_images.txt", "r") as file:
				for i, line in enumerate(file.readlines()):
					line = line.removesuffix("\n")
					self.changePreviewImage(i, EXPORT_DIR + "/" + line)
					self.cb_previews[i].set_active(self.extracted.index(line))
		except:
			pass


	def showMainWindow(self):
		window = self.builder.get_object("main_window")
		window.show_all()

		Gtk.main()


	def changePreviewImage(self, imageId: int, imageURI: str):
		pixbuf = GdkPixbuf.Pixbuf.new_from_file(DIR + "/" + imageURI)
		pixbuf = pixbuf.scale_simple(300, 200, GdkPixbuf.InterpType.BILINEAR)

		self.img_previews[imageId].set_from_pixbuf(pixbuf)


	def extractHeifImages(self, imageURI: str):
		imageURI = imageURI.replace("%20", "\ ")
		
		filename = imageURI[imageURI.rfind("/"):imageURI.rfind(".")]

		self.wipeImages()
		os.system("heif-convert " + imageURI + " " + DIR + "/" + EXPORT_DIR + filename + ".jpg")


	def wipeImages(self):
		for file in glob.glob(DIR + "/" + EXPORT_DIR + "/*"):
			os.remove(file)


	def changePreviewSpinners(self, options: list):
		for option in options:
			self.ls_preview.append([option])


	def createExtracted(self):
		self.extracted = os.listdir(DIR + "/" + EXPORT_DIR)
		self.extracted.sort()


	########## UI Signals ##########

	def onHeifSelected(self, fc):
		# Get the URI to the file
		uri = fc.get_file().get_uri()
		uri = uri[7:]

		self.extractHeifImages(uri)
		self.createExtracted()
		self.changePreviewSpinners(self.extracted)


	def onRadioImageSet(self, rb):
		""" UI Signal, if the radio buttons are toggled

		Args:
			rb (GtkRadioButton): The toggled RadioButton
		"""
		self.imageSetText.set_visible(rb.get_active())
		self.imageSetCb.set_visible(rb.get_active())

		self.fileChooserText.set_visible(not rb.get_active())
		self.fileChooserFc.set_visible(not rb.get_active())


	def onPreviewComboboxSelected(self, cb):
		number = Gtk.Buildable.get_name(cb)
		number = number[number.rfind("_") + 1:]
		
		self.changePreviewImage(int(number) - 1, EXPORT_DIR + "/" + self.extracted[cb.get_active()])


	def onApply(self, *args):
		buffer = []

		for cb in self.cb_previews:
			if cb.get_active() != -1:
				buffer.append(self.extracted[cb.get_active()])
			else:
				buffer.append(buffer[len(buffer) - 1])
		
		with open(DIR + "/selected_images.txt", "w") as file:
			for buff in buffer:
				file.write(buff + "\n")
		
		# todo
		Gtk.main_quit()


	def onDestroy(self, *args):
		Gtk.main_quit()


ic = ImageConfigurator()
ic.showMainWindow()

