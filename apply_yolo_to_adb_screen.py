# This code is written at BigVision LLC. It is based on the OpenCV project. It is subject to the license terms in the LICENSE file found in this distribution and at http://opencv.org/license.html

# Usage example:  python3 object_detection_yolo.py --video=run.mp4
#                 python3 object_detection_yolo.py --image=bird.jpg

import io

from detectors.cards import *
from detectors.mana import *
from detectors.units import *

# Process inputs
winName = 'Deep learning object detection in OpenCV'
cv.namedWindow(winName, cv.WINDOW_NORMAL)

outputFile = "yolo_out_py.avi"

from adb.client import Client as AdbClient

client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
print(devices)
device = devices[0]
width, height = Image.open(io.BytesIO(device.screencap())).size

# Get the video writer initialized to save the output video
vid_writer = cv.VideoWriter(outputFile, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (round(width), round(height)))

while cv.waitKey(1) < 0:

    # get frame from the video
    # hasFrame, frame = cap.read()
    screen = None
    try:
        screen = Image.open(io.BytesIO(device.screencap()))
    except RuntimeError:
        screen = None

    if screen is not None:
        # todo parse only in game?
        mana = parseMana(screen)
        cards = parseCards(screen)

        # https://stackoverflow.com/a/39270509/699934
        frame = np.array(np.asarray(screen, dtype='uint8')[..., :3][:, :, ::-1])

        predictions = predictUnits(frame)

        drawPredictions(frame, predictions)

        cv.putText(frame, 'Mana: %s, cards: %s' % (str(mana), str(cards)), (0, 35), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                   (255, 255, 255))

        vid_writer.write(frame.astype(np.uint8))

        cv.imshow(winName, frame)
    else:
        print('wait for device...')
