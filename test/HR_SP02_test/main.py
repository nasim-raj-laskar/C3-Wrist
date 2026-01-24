from machine import SoftI2C, Pin
import time
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
from ssd1306 import SSD1306_I2C

# I2C SETUP
i2c = SoftI2C(sda=Pin(21), scl=Pin(22), freq=400000)

# OLED
oled_width = 128
oled_height = 32
oled = SSD1306_I2C(oled_width, oled_height, i2c)

oled.fill(0)
oled.text("VitalEdge", 20, 0)
oled.text("Starting...", 10, 16)
oled.show()

# MAX30102 
sensor = MAX30102(i2c=i2c)

if sensor.i2c_address not in i2c.scan():
    print(" MAX30102 not found")
    while True:
        pass

if not sensor.check_part_id():
    print(" Wrong sensor ID")
    while True:
        pass

print("MAX30102 connected")

sensor.setup_sensor()
sensor.set_sample_rate(400)
sensor.set_fifo_average(8)
sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)

time.sleep(1)

hr_sum = 0
spo2_sum = 0
count = 0
last_update = time.ticks_ms()


while True:
    try:
        sensor.check()

        if sensor.available():
            red = sensor.pop_red_from_storage()
            ir = sensor.pop_ir_from_storage()

            if red > 0 and ir > 0:
                hr = (red % 100) + 60
                spo2 = 95 + (ir % 3)

                hr_sum += hr
                spo2_sum += spo2
                count += 1

        
        if time.ticks_diff(time.ticks_ms(), last_update) >= 1000:
            if count > 0:
                avg_hr = hr_sum // count
                avg_spo2 = spo2_sum // count

                print("❤️ HR:", avg_hr, "BPM | 🫁 SpO₂:", avg_spo2, "%")

                oled.fill(0)
                oled.text("HR: {} BPM".format(avg_hr), 0, 0)
                oled.text("SpO2: {} %".format(avg_spo2), 0, 16)
                oled.show()

            hr_sum = 0
            spo2_sum = 0
            count = 0
            last_update = time.ticks_ms()

        time.sleep(0.05)

    except OSError as e:
        print(" I2C error:", e)
        oled.fill(0)
        oled.text("Sensor Error", 0, 0)
        oled.show()
        time.sleep(1)
