import time

import cv2
import numpy as np

start = time.time()

screen = cv2.imread("screens/1539379684.jpg", cv2.IMREAD_GRAYSCALE)
card = cv2.resize(cv2.imread("cards/tornado.png", cv2.IMREAD_GRAYSCALE),
                  (0, 0), fx=0.5, fy=0.5)

MIN_MATCH_COUNT = 8

kaze = cv2.KAZE_create(False, False, 0.0001, 5, 5)

kp1, des1 = kaze.detectAndCompute(card, None)
kp2, des2 = kaze.detectAndCompute(screen, None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=1)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

# Match descriptors.
matches = flann.knnMatch(des1, des2, k=2)

good = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good.append(m)

matchesMask = None
print(len(good))
if len(good) > MIN_MATCH_COUNT:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()

    h, w = card.shape
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)

    screen = cv2.polylines(screen, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
else:
    print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
    matchesMask = None

draw_params = dict(matchColor=(255, 255, 0),  # draw matches in green color
                   singlePointColor=None,
                   matchesMask=matchesMask,  # draw only inliers
                   flags=2)

# Sort them in the order of their distance.
# matches = sorted(matches, key = lambda x:x.distance)

end = time.time()

print(end - start)

# Draw first 10 matches.
img3 = cv2.drawMatches(card, kp1, screen, kp2, good, None, **draw_params)

cv2.imshow("preview", img3)
cv2.waitKey(0)
cv2.destroyAllWindows()
