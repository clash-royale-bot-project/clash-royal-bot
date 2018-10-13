import io

from actions.touch import *
from detectors.cards import *
from detectors.mana import *
from detectors.units import *
# Process inputs
from strategy.strategy import predictions_to_actions
from utils import copy_image_to_np_array

if __name__ == '__main__':
    winName = 'Clash Royale AI'
    cv.namedWindow(winName, cv.WINDOW_NORMAL)

    outputFile = "yolo_out_py.avi"

    from adb.client import Client as AdbClient

    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    print(devices)
    device = devices[0]
    width, height = Image.open(io.BytesIO(device.screencap())).size

    # Get the video writer initialized to save the output video
    # vid_writer = cv.VideoWriter(outputFile, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (round(width), round(height)))

    classes = loadUnitsNNClasses()

    next_actions = list()

    same_cards_stable = 3
    last_cards = []
    def is_cards_prediction_stable():
        if len(last_cards) >= same_cards_stable:
            head = last_cards[0]
            return all(cards == head for cards in last_cards[1:same_cards_stable])
        else:
            return False


    while cv.waitKey(1) < 0:
        if len(next_actions) == 0:
            screen = Image.open(io.BytesIO(device.screencap()))

            # todo parse only in game?
            mana = parseMana(screen)

            frame = copy_image_to_np_array(screen)

            if mana is not None:
                cards = parse_cards(screen)
                last_cards.insert(0, cards)
                last_cards = last_cards[0:same_cards_stable]

                if cards is not None and is_cards_prediction_stable():
                    predictions = predict_units(screen)

                    draw_predictions(frame, classes, predictions)

                    newActions = predictions_to_actions(screen, predictions, classes, mana, cards)

                    next_actions.extend(list(newActions))

                    cv.putText(frame, 'Mana: %s, cards: %s' % (str(mana), str(cards)), (0, 35), cv.FONT_HERSHEY_SIMPLEX,
                               0.5,
                               (255, 255, 255))
                print(last_cards)

            # vid_writer.write(frame.astype(np.uint8))

            cv.imshow(winName, frame)

        else:
            action, params = next_actions.pop(0)

            if action == 'click':
                print('making click at [{},{}]'.format(params[0], params[1]))
                tap(device, params[0], params[1])
