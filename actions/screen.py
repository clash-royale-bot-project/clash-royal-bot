import io
import time

from PIL import Image
from screenshot.screencapture import screenshot_window

from adb.client import Client as AdbClient

file = '/tmp/player_shoot.png'

# not so good
def screenshoot():
    screenshot_window("player", filename='/tmp/player_shoot.png')
    player = Image.open('/tmp/player_shoot.png')
    player = player.crop((84, 112, 1044, 1713))
    player.thumbnail((480,800), Image.ANTIALIAS)
    return player

def screencap(device):
    return Image.open(io.BytesIO(device.screencap()))

if __name__ == '__main__':
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    print(devices)
    device = devices[0]
    while True:
        s = time.time()
        screencap(device)
        print(time.time() - s)