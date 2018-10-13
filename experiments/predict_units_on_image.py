import numpy as np
from PIL import Image

from detectors.cards import parse_cards
from detectors.mana import parseMana
from detectors.units import loadUnitsNNClasses, predict_units, draw_predictions
from utils import copy_image_to_np_array

if __name__ == '__main__':
    screen = Image.open("/Users/tolsi/Documents/clash_royale_bot/bot/bot/screens/1539357173.jpg")
    frame = copy_image_to_np_array(screen)
    classes = loadUnitsNNClasses()
    predictions = predict_units(screen)
    draw_predictions(frame, classes, predictions)
    screen.show()
    Image.fromarray(np.uint8(frame[:, :, ::-1])).show()