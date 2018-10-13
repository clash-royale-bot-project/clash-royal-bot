import time

from adb.client import Client as AdbClient

client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
print(devices)
device = devices[0]
device.screencap()


def tap(x, y):
    print(device.shell('input tap {} {}'.format(x, y)))


def shoot():
    return device.screencap()


tap(40, 750)
time.sleep(1)
tap(200, 750)
time.sleep(1)
# Image.open(io.BytesIO(shoot())).show()

# from adb import ADB
#
# debug = ADB()
#
# print(debug.devices())
#
# debug.screenShot("/tmp/saved.png")
