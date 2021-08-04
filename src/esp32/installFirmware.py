"""
    script for install last stable ESP32 firmware

"""

import tempfile
import os
import wget

from serial.tools.list_ports import comports

linkFirmware = 'https://micropython.org/resources/firmware/esp32-20210623-v1.16.bin'
serialPort = [port.device for port in comports() if port.vid == 4292 and port.pid == 60000][0] or 'COM3'

temp = tempfile.gettempdir()
print(wget.download(url=linkFirmware,
                    out=temp + '/esp32Firmware.bin'))

print(os.system(f'python -m esptool --port {serialPort} erase_flash', ))
print(os.system(
    f'python -m esptool --chip esp32 --port {serialPort} write_flash -z 0x1000 {temp + "/esp32Firmware.bin"}'))

os.remove(temp + '/esp32Firmware.bin')
