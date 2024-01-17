import os

class Images:
	def __init__(self) -> None:
		pass

	def get_images_from_folder(self, URI: str) -> list:
		items = []

		for file in os.listdir(URI):
			if file.endswith("jpg") or file.endswith("jpeg") or file.endswith("png") or file.endswith("bmp"):
				items.append(file)

		items.sort()
		return items