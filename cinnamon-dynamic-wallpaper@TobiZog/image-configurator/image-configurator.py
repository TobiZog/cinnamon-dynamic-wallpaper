import gi, os, glob, json

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

DIR = os.path.dirname(os.path.abspath(__file__))
UI_FILE = DIR + "/image-configurator.glade"
EXPORT_DIR = "extracted"


class ImageConfigurator:
	def __init__(self) -> None:
		########### Class variables ###########
		self.pref_vars = [
			"etr_img_morning_twilight",
			"etr_img_sunrise",
			"etr_img_morning",
			"etr_img_noon",
			"etr_img_afternoon",
			"etr_img_evening",
			"etr_img_sunset",
			"etr_img_night_twilight",
			"etr_img_night"
		]

		self.pref_path = os.path.expanduser("~") + \
			"/.config/cinnamon/spices/cinnamon-dynamic-wallpaper@TobiZog/cinnamon-dynamic-wallpaper@TobiZog.json"


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


		# Load preferences
		self.createExtracted()
		self.loadFromSettings()



	def showMainWindow(self):
		window = self.builder.get_object("main_window")
		window.show_all()

		Gtk.main()

	
	def loadFromSettings(self):
		with open(self.pref_path, "r") as pref_file:
			pref_data = json.load(pref_file)

		for i, val in enumerate(self.pref_vars):
			try:
				self.changePreviewImage(i, EXPORT_DIR + "/" + pref_data[val]['value'])
				self.cb_previews[i].set_active(self.extracted.index(pref_data[val]['value']))
			except:
				pass





	def writeToSettings(self):
		with open(self.pref_path, "r") as pref_file:
			pref_data = json.load(pref_file)

		for i, val in enumerate(self.pref_vars):
			pref_data[val]['value'] = self.extracted[self.cb_previews[i].get_active()]

		with open(self.pref_path, "w") as pref_file:
			json.dump(pref_data, pref_file, separators=(',', ':'), indent=4)

		


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


	def createExtracted(self):
		self.extracted = os.listdir(DIR + "/" + EXPORT_DIR)
		self.extracted.sort()

		self.ls_preview.clear()

		for option in self.extracted:
			self.ls_preview.append([option])


	########## UI Signals ##########

	def onRadioImageSet(self, rb):
		""" UI Signal, if the radio buttons are toggled

		Args:
			rb (GtkRadioButton): The toggled RadioButton
		"""
		self.imageSetText.set_visible(rb.get_active())
		self.imageSetCb.set_visible(rb.get_active())

		self.fileChooserText.set_visible(not rb.get_active())
		self.fileChooserFc.set_visible(not rb.get_active())


	def onHeifSelected(self, fc):
		# Get the URI to the file
		uri = fc.get_file().get_uri()
		uri = uri[7:]

		self.extractHeifImages(uri)
		self.createExtracted()


	def onPreviewComboboxSelected(self, cb):
		number = Gtk.Buildable.get_name(cb)
		number = number[number.rfind("_") + 1:]
		
		self.changePreviewImage(int(number) - 1, EXPORT_DIR + "/" + self.extracted[cb.get_active()])


	def onApply(self, *args):
		self.writeToSettings()

		Gtk.main_quit()


	def onDestroy(self, *args):
		Gtk.main_quit()


ic = ImageConfigurator()
ic.showMainWindow()

