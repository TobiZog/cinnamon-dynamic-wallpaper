import os

class Images:
	def __init__(self) -> None:
		pass

	def get_images_from_folder(self, URI: str) -> list:
		items = os.listdir(URI)
		items.sort()
		return items