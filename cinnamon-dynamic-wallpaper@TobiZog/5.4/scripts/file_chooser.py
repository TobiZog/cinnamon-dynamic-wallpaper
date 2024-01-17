import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class FileChooser(Gtk.Window):
  def __init__(self) -> None:
    super().__init__()

  def on_btn_source_folder_clicked(self) -> str:
    dialog = Gtk.FileChooserDialog(
      title= "Please choose a folder with images",
      parent=self,
      action=Gtk.FileChooserAction.SELECT_FOLDER
    )

    dialog.add_buttons(
      Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK
    )

    dialog.set_default_size(800, 400)

    response = dialog.run()

    if response == Gtk.ResponseType.OK:
      location = dialog.get_filename()
    elif response == Gtk.ResponseType.CANCEL:
      location = ""

    dialog.destroy()

    return location
