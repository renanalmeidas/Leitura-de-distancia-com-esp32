import utime
import ubinascii
import machine
from umqtt.simple import MQTTClient
from machine import Pin
from hcsr04 import HCSR04
from utime import sleep
import uasyncio


SERVER = "192.168.30.253"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = "laura".encode('utf-8')
led = Pin(2, Pin.OUT)


def sub_cb(topic, msg):
    print(msg)
    if msg == b"1":
        led.on()
    else:
        led.off()


c = MQTTClient(CLIENT_ID, SERVER)
c.set_callback(sub_cb)
c.connect()
c.subscribe("laura/led")
sensor = HCSR04(trigger_pin=32, echo_pin=34)


async def recebe(c):
    while True:
        if c.check_msg():
            c.wait_msg()
        await uasyncio.sleep_ms(100)

async def envia(c):
    lista = []
    while True:
        if len(lista) > 5:
            del lista[0]
        lista.append(sensor.distance_cm())
        c.publish("laura/sensor".encode(), "{:.2f}".format(sum(lista)/len(lista)).encode())
        await uasyncio.sleep_ms(100)


loop = uasyncio.get_event_loop()
loop.create_task(envia(c))
loop.create_task(recebe(c))
loop.run_forever()
