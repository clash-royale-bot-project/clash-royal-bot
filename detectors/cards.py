import os
import time

import cv2
import numpy as np
from PIL import Image

cards_path = '/Users/tolsi/Documents/clash_royale_bot/bot/cards'

detect_card_1_area = (114, 650, 194, 760)
detect_card_2_area = (200, 650, 280, 760)
detect_card_3_area = (284, 650, 364, 760)
detect_card_4_area = (370, 650, 450, 760)
all_cards_detect_areas = [detect_card_1_area, detect_card_2_area, detect_card_3_area, detect_card_4_area]

real_card_1_area = (119, 665, 189, 750)
real_card_2_area = (205, 665, 275, 750)
real_card_3_area = (289, 665, 359, 750)
real_card_4_area = (375, 665, 445, 750)
all_cards_real_areas = [detect_card_1_area, detect_card_2_area, detect_card_3_area, detect_card_4_area]

cards_area = (114, 650, 450, 760)

# region parse cards inits
kaze = cv2.KAZE_create(False, False, 0.0001, 5, 5)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=1)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)


# endregion

def detectCardPos(x, y):
    for idx, val in enumerate(all_cards_detect_areas):
        if val[0] >= x and val[1] >= y and val[2] <= x and val[3] <= y:
            return idx
    return None


def parse_cards(img):
    cropped_cards = img.crop(cards_area)
    cropped_cards = np.asarray(cropped_cards, dtype='uint8')[..., :3][:, :, ::-1]
    kp2, des2 = kaze.detectAndCompute(cropped_cards, None)
    if des2 is not None:
        results = []
        for card_name, kp1, des1 in card_and_points:
            matches = flann.knnMatch(des1, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.7 * n.distance:
                    good.append(m)
            good = sorted(good, key=lambda x: -x.distance)
            results.append((card_name, good))
        # by points count
        results = sorted(results, key=lambda x: len(x[1]))
        # take only best 4
        results = results[-4:]
        if any(len(x[1]) < 2 for x in results):
            return None
        else:
            # by point x
            results = sorted(results, key=lambda x: kp2[x[1][-1].trainIdx].pt[0])
            return list(map(lambda x: x[0], results))
    else:
        return None


# region init cards
card_and_points = []
for filename in os.listdir(cards_path):
    if filename.endswith('.png') and not filename.startswith('.'):
        image = cv2.resize(cv2.imread(os.path.join(cards_path, filename), cv2.IMREAD_GRAYSCALE), (0, 0), fx=0.5, fy=0.5)
        kp, des = kaze.detectAndCompute(image, None)
        card_and_points.append((filename.replace('.png', ''), kp, des))
# endregion

if __name__ == '__main__':
    start = time.time()
    print(parse_cards(Image.open("/Users/tolsi/Documents/clash_royale_bot/bot/bot/screens/1539379684.jpg")))
    end = time.time()
    print(end - start)
