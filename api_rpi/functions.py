import RPi.GPIO as GPIO
import time

LED_rosu = 4
LED_verde = 27

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_rosu, GPIO.OUT)
GPIO.setup(LED_verde, GPIO.OUT)
GPIO.setup(LED_rosu, 0)
GPIO.setup(LED_verde, 1)

def LED_rosu_Blink():
    GPIO.setup(LED_rosu, 0)

def LED_verde_Blink():
    GPIO.setup(LED_rosu, 1)
    GPIO.setup(LED_verde, 1)
    time.sleep(0.2)
    GPIO.setup(LED_verde, 0)
    time.sleep(0.2)
    GPIO.setup(LED_verde, 1)
    time.sleep(0.2)
    GPIO.setup(LED_verde, 0)
    time.sleep(0.2)
    GPIO.setup(LED_verde, 0)
    time.sleep(3)
    GPIO.setup(LED_verde, 1)
    GPIO.setup(LED_rosu, 0)