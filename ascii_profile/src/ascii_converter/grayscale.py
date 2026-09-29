# ascii_profile/src/ascii_converter/grayscale.py

from PIL import Image, ImageEnhance, ImageOps


def convert_to_grayscale(image: Image.Image, contrast: float = 1.0) -> Image.Image:
	"""Convert an image to grayscale and apply a configurable contrast factor.

	A contrast value of 1.0 preserves the grayscale values. Values greater
	than 1.0 increase contrast, while values between 0.0 and 1.0 reduce it.
	"""
	if contrast < 0:
		raise ValueError("Contrast must be greater than or equal to 0.")

	grayscale_image = ImageOps.grayscale(image)
	return ImageEnhance.Contrast(grayscale_image).enhance(contrast)
