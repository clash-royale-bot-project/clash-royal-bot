from PIL import ImageOps
from pytesseract import image_to_string

mana_area = (135, 760, 163, 784)


def parseMana(img):
    cropped_img = img.crop(mana_area)
    cropped_img = cropped_img.convert('L').point(lambda x: 255 if x > 250 else 0, mode='1')
    cropped_img = ImageOps.invert(cropped_img.convert('L'))
    cropped_img = cropped_img.convert('1')
    try:
        result = int(image_to_string(cropped_img, config='-c tessedit_char_whitelist=0123456789 --psm 7'))
    except ValueError:
        result = None
    return result
