import random
import time

from PIL import Image

from detectors.cards import parse_cards, all_cards_real_areas
from detectors.mana import parseMana
from detectors.units import predict_units, loadUnitsNNClasses
from strategy.data import cards_price, unit_type

real_field_area = (58, 110, 423, 598)

# from 1
def field_position_center(x, y):
    # height: 14 + 1 river + 14
    # width: 18
    assert x >= 0 and x < 18
    assert y >= 0 and y < 29
    from_real_x = real_field_area[0] + (x-1) * 20
    from_real_y = real_field_area[1] + (y-1) * 17
    return random_pos_in_area((from_real_x, from_real_y, from_real_x + 20, from_real_y + 17))


def random_pos_in_area(area):
    assert len(area) == 4
    return (random.randrange(area[0], area[2]), random.randrange(area[1], area[3]))


def card_position_center(index):
    assert index >= 0 and index <= 3
    area = all_cards_real_areas[index]
    return random_pos_in_area(area)


def predictions_to_actions(screen, predictions, classes, mana, cards):
    my_allowed_cards = list(filter(lambda p: cards_price.get(p[1], 11) <= mana, enumerate(cards)))
    actions = []
    if len(my_allowed_cards) > 0:
        # todo let's think about it later
        first_allowed_unit = next((p for p in my_allowed_cards if unit_type(p[1]) == 'unit'), None)
        if first_allowed_unit is not None:
            actions = [(first_allowed_unit[0], field_position_center(6, 25))]
            print('make actions: {} as {}'.format(str(first_allowed_unit), str(actions)))
    clicks = []
    for card_index, to in actions:
        clicks.append(('click', card_position_center(card_index)))
        clicks.append(('click', to))
    return clicks

if __name__ == '__main__':
    start = time.time()
    screen = Image.open("screens/1539357975.jpg")
    classes = loadUnitsNNClasses()
    predictions = predict_units(screen)
    mana = parseMana(screen)
    cards = parse_cards(screen)
    clicks = predictions_to_actions(screen, predictions, classes, mana, cards)
    print(clicks)
    end = time.time()
    print(end - start)
