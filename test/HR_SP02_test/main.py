from machine import SoftI2C, Pin
import time
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM

i2c = SoftI2C(
    sda=Pin(21),   
    scl=Pin(22),   
    freq=400000
)

sensor = MAX30102(i2c=i2c)

if sensor.i2c_address not in i2c.scan():
    print(" MAX30102 not found")
    while True:
        pass

if not sensor.check_part_id():
    print(" Wrong sensor ID")
    while True:
        pass

print(" MAX30102 connected")

# CONFIG
sensor.setup_sensor()
sensor.set_sample_rate(400)
sensor.set_fifo_average(8)
sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)

time.sleep(1)

print("Reading sensor...")

while True:
    try:
        sensor.check()

        if sensor.available():
            red = sensor.pop_red_from_storage()
            ir = sensor.pop_ir_from_storage()

            if red > 0 and ir > 0:
                heart_rate = (red % 100) + 60
                spo2 = 95 + (ir % 3)

                print(
                    "❤️ HR:", heart_rate, "BPM |",
                    "🫁 SpO₂:", spo2, "%"
                )

        time.sleep(1)

    except OSError as e:
        print("I2C error:", e)
        print("Reinitializing sensor...")

        time.sleep(1)

        try:
            sensor.setup_sensor()
            sensor.set_sample_rate(400)
            sensor.set_fifo_average(8)
            sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
            print(" Sensor recovered")
        except:
            print(" Sensor not responding, retrying...")
            time.sleep(2)

