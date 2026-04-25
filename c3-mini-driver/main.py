from machine import Pin
import time

# Try GPIO 8 first (most common for C3 SuperMini)
led = Pin(8, Pin.OUT)

while True:
    led.on()
    print("LED ON")
    time.sleep(1)
    
    led.off()
    print("LED OFF")
    time.sleep(1)
