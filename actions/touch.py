import time

from adb.client import Client as AdbClient

def tap(device, x, y):
    print(device.shell('input tap {} {}'.format(x, y)))

if __name__ == '__main__':
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    print(devices)
    device = devices[0]
    device.screencap()
    tap(40, 750)
    time.sleep(1)
    tap(200, 750)
    time.sleep(1)