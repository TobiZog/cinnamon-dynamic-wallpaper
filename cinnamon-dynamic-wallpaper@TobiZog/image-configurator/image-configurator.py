import gi, os, glob, json, shutil, enum, threading

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
PROG_DIR = PROJECT_DIR + "/image-configurator"
EXPORT_DIR = PROG_DIR + "/extracted"
RES_DIR = PROJECT_DIR + "/res"
UI_PATH = PROG_DIR + "/image-configurator.glade"
PREF_PATH = os.path.expanduser("~") + \
	"/.config/cinnamon/spices/cinnamon-dynamic-wallpaper@TobiZog/cinnamon-dynamic-wallpaper@TobiZog.json"

class Source(enum.Enum):
	RESSOURCES = 0
	EXPORT = 1
	SET = 2


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

		########### Create the folder ###########
		try:
			os.mkdir(EXPORT_DIR)
		except:
			pass

		try:
			os.mkdir(RES_DIR + "/custom_images")
		except:
			pass

		########### GTK stuff ###########
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_PATH)
		self.builder.connect_signals(self)

		########### Glade Ressources ###########
		self.rb_included_image_set = self.builder.get_object("rb_included_image_set")
		self.rb_external_image_set = self.builder.get_object("rb_external_image_set")

		self.lb_image_set = self.builder.get_object("lb_image_set")
		self.cb_image_set = self.builder.get_object("cb_image_set")

		self.lb_heic_file = self.builder.get_object("lb_heic_file")
		self.fc_heic_file = self.builder.get_object("fc_heic_file")
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

		# The GtkStack
		self.stack_main = self.builder.get_object("stack_main")
		self.stack_main.add_named(self.builder.get_object("page_config"), "config")
		self.stack_main.add_named(self.builder.get_object("page_load"), "load")
		self.stack_main.set_visible_child_name("config")
		

		########### Load predefinitions and settings ###########
		self.image_set_list_store.append(["Big Sur Beach 2"])
		self.image_set_list_store.append(["Firewatch"])
		self.image_set_list_store.append(["Lakeside"])
		# todo

		# Load preferences
		self.loadFromSettings()


	def showMainWindow(self):
		""" Opens the main window, starts the Gtk main routine
		"""
		window = self.builder.get_object("main_window")
		window.show_all()

		Gtk.main()

	
	def loadFromSettings(self):
		""" Load preferences from the Cinnamon preference file
		"""
		# Load the settings
		with open(PREF_PATH, "r") as pref_file:
			pref_data = json.load(pref_file)


		# Use the settings
		if pref_data["etr_choosen_image_set"]["value"] == "custom":
			self.image_source = Source.RESSOURCES
		else:
			#todo
			pass

		self.createExtracted()
		
		for i, val in enumerate(self.pref_vars):
			try:
				self.changePreviewImage(i, RES_DIR + "/custom_images/" + pref_data[val]['value'])
				self.cb_previews[i].set_active(self.extracted.index(pref_data[val]['value']))
			except:
				pass
	

	def writeToSettings(self):
		""" Save preferences to the Cinnamon preference file
		"""
		# Load the settings
		with open(PREF_PATH, "r") as pref_file:
			pref_data = json.load(pref_file)


		# Update the settings
		for i, val in enumerate(self.pref_vars):
			pref_data[val]['value'] = self.extracted[self.cb_previews[i].get_active()]


		if self.rb_included_image_set:
			#pref_data["etr_choosen_image_set"]["value"] = self.cb_image_set.
			# todo
			pass
		else:
			pref_data["etr_choosen_image_set"]["value"] = "custom"


		# Write the settings
		with open(self.pref_path, "w") as pref_file:
			json.dump(pref_data, pref_file, separators=(',', ':'), indent=4)


	def changePreviewImage(self, imageId: int, imageURI: str):
		""" Exchanges the image in the preview

		Args:
			imageId (int): The number of the preview (0-8)
			imageURI (str): URI to the new image
		"""
		pixbuf = GdkPixbuf.Pixbuf.new_from_file(imageURI)
		pixbuf = pixbuf.scale_simple(300, 200, GdkPixbuf.InterpType.BILINEAR)

		self.img_previews[imageId].set_from_pixbuf(pixbuf)


	def extractHeifImages(self, imageURI: str):
		""" Extract all images in a heif file

		Args:
			imageURI (str): URI to the heif file
		"""
		imageURI = imageURI.replace("%20", "\ ")
		
		filename = imageURI[imageURI.rfind("/") + 1:imageURI.rfind(".")]

		self.image_source = Source.EXPORT

		self.wipeImages(Source.EXPORT)
		os.system("heif-convert " + imageURI + " " + EXPORT_DIR + "/" + filename + ".jpg")

		self.createExtracted()


	def wipeImages(self, source: Source):
		""" Removes all image of a folder

		Args:
			source (Source): Choose the folder by selecting the Source
		"""
		if source == Source.EXPORT:
			dir = EXPORT_DIR + "/*"
		elif source == Source.RESSOURCES:
			dir = RES_DIR + "/custom_images/*"
		
		for file in glob.glob(dir):
			os.remove(file)


	def createExtracted(self):
		""" Create the extracted images array
		"""
		if self.image_source == Source.RESSOURCES:
			self.extracted = os.listdir(RES_DIR + "/custom_images")
		elif self.image_source == Source.EXPORT:
			self.extracted = os.listdir(EXPORT_DIR)

		self.extracted.sort()
		self.ls_preview.clear()

		for option in self.extracted:
			self.ls_preview.append([option])

		self.stack_main.set_visible_child_name("config")


	def copyToSource(self):
		""" Copies the extracted images to "res/"
		"""
		self.wipeImages(Source.RESSOURCES)

		for image in os.listdir(EXPORT_DIR):
			shutil.copy(EXPORT_DIR + "/" + image, RES_DIR + "/custom_images/" + image)


	def imageSetVisibility(self, source: Source):
		""" Toggle the visibility of the option in the "Image set" box

		Args:
			source (Source): Toggle by type of Source
		"""
		self.lb_image_set.set_visible(source == Source.SET)
		self.cb_image_set.set_visible(source == Source.SET)

		self.lb_heic_file.set_visible(source != Source.SET)
		self.fc_heic_file.set_visible(source != Source.SET)



	########## UI Signals ##########

	def onRadioImageSet(self, rb):
		""" UI signal if the radio buttons are toggled

		Args:
			rb (GtkRadioButton): The toggled RadioButton
		"""
		if rb.get_active():
			self.imageSetVisibility(Source.SET)
		else:
			self.imageSetVisibility(Source.EXPORT)


	def onHeifSelected(self, fc):
		""" UI signal if the filechooser has a file selected

		Args:
			fc (filechooser): The selected filechooser
		"""
		# Get the URI to the file
		uri = fc.get_file().get_uri()
		uri = uri[7:]

		self.stack_main.set_visible_child_name("load")

		thread = threading.Thread(target=self.extractHeifImages, args=(uri, ))
		thread.daemon = True
		thread.start()		


	def onPreviewComboboxSelected(self, cb):
		""" UI signal if one of the preview combobox is selected

		Args:
			cb (ComboBox): The selected combobox
		"""
		number = Gtk.Buildable.get_name(cb)
		number = number[number.rfind("_") + 1:]
		
		# todo
		if self.image_source == Source.RESSOURCES:
			self.changePreviewImage(int(number) - 1, RES_DIR + "/custom_images/" + self.extracted[cb.get_active()])
		elif self.image_source == Source.EXPORT:
			self.changePreviewImage(int(number) - 1, EXPORT_DIR + "/" + self.extracted[cb.get_active()])


	def onApply(self, *args):
		""" UI signal if the user presses the "Apply" button
		"""
		self.writeToSettings()
		self.copyToSource()

		Gtk.main_quit()


	def onDestroy(self, *args):
		""" UI signal if the window is closed by the user
		"""
		Gtk.main_quit()


if __name__ == "__main__":
	ic = ImageConfigurator()
	ic.showMainWindow()
