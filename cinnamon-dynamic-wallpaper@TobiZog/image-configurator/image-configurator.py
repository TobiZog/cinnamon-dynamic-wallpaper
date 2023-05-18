import gi, os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

UI_FILE = os.path.dirname(os.path.abspath(__file__)) + "/image-configurator.glade"

class ImageConfigurator:
	def __init__(self) -> None:
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		# Get all resources from the glade file
		self.imageSetText = self.builder.get_object("lb_image_set")
		self.imageSetCb = self.builder.get_object("cb_image_set")

		self.fileChooserText = self.builder.get_object("lb_heic_file")
		self.fileChooserFc = self.builder.get_object("fc_heic_file")
		self.image_set_list_store = self.builder.get_object("image_set_list_store")

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

		# Predefinition
		self.image_set_list_store.append(["Big Sur Beach 2"])
		self.image_set_list_store.append(["Firewatch"])
		self.image_set_list_store.append(["Lakeside"])


	def showMainWindow(self):
		window = self.builder.get_object("main_window")
		window.show_all()

		Gtk.main()


	def changeImage(self, imageId: int, imageURI: str):
		self.img_previews[imageId].set_from_file(os.path.dirname(os.path.abspath(__file__)) + "/" + imageURI)


	def onRadioIncludedImageSet(self, rb):
		if rb.get_active():
			self.imageSetText.set_visible(True)
			self.imageSetCb.set_visible(True)

			self.fileChooserText.set_visible(False)
			self.fileChooserFc.set_visible(False)


	def onRadioExternalImageSet(self, rb):
		if rb.get_active():
			self.fileChooserText.set_visible(True)
			self.fileChooserFc.set_visible(True)
			
			self.imageSetText.set_visible(False)
			self.imageSetCb.set_visible(False)


	def onApply(self, *args):
		# todo
		Gtk.main_quit()


	def onDestroy(self, *args):
		Gtk.main_quit()


ic = ImageConfigurator()
ic.showMainWindow()

