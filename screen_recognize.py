from PIL import Image, ImageOps
from pytesseract import image_to_string

mana_area = (135, 760, 163, 784)

card_1_area = (114, 650, 194, 760)
card_2_area = (200, 650, 280, 760)
card_3_area = (284, 650, 364, 760)
card_4_area = (370, 650, 450, 760)
cards_area = (114, 650, 450, 760)

def parseMana(img):
    cropped_img = img.crop(mana_area)
    cropped_img = cropped_img.convert('L').point(lambda x : 255 if x > 250 else 0, mode='1')
    cropped_img = ImageOps.invert(cropped_img.convert('L'))
    cropped_img = cropped_img.convert('1')
    cropped_img.show()
    try:
        result = int(image_to_string(cropped_img,config='-c tessedit_char_whitelist=0123456789 --psm 7'))
    except ValueError:
        result = None
    return result

def parseCards(img):
    cropped_cards = img.crop(cards_area)
    cropped_cards.show()

print(parseCards(Image.open('/Users/tolsi/Documents/clash_royale_bot/bot/bot/screens/1539357970.jpg')))