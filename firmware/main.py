from machine import I2C, Pin                                #type: ignore
import time
import ssd1306

# OLED
i2c = I2C(0, scl=Pin(7), sda=Pin(6), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

# Buttons
btn_next = Pin(21, Pin.IN, Pin.PULL_UP)
btn_select = Pin(20, Pin.IN, Pin.PULL_UP)
btn_action = Pin(10, Pin.IN, Pin.PULL_UP)

# LED
led = Pin(9, Pin.OUT)

# Time
hour, minute, second = 12, 0, 0

# Stopwatch
sw_running = False
sw_time = 0

# UI
mode = "clock"
menu_index = 0
set_stage = None

menu_items = ["Set Time", "LED", "Stopwatch"]

# --- BIG DIGITS ---
digits = {
"0":["01110","10001","10011","10101","11001","10001","01110"],
"1":["00100","01100","00100","00100","00100","00100","01110"],
"2":["01110","10001","00001","00010","00100","01000","11111"],
"3":["11110","00001","00001","01110","00001","00001","11110"],
"4":["00010","00110","01010","10010","11111","00010","00010"],
"5":["11111","10000","11110","00001","00001","10001","01110"],
"6":["00110","01000","10000","11110","10001","10001","01110"],
"7":["11111","00001","00010","00100","01000","01000","01000"],
"8":["01110","10001","10001","01110","10001","10001","01110"],
"9":["01110","10001","10001","01111","00001","00010","11100"],
":":["00000","00100","00100","00000","00100","00100","00000"]
}

def draw_big_digit(char, x, y, scale=3):
    pattern = digits.get(char)
    if not pattern:
        return
    for row, line in enumerate(pattern):
        for col, pixel in enumerate(line):
            if pixel == "1":
                oled.fill_rect(
                    x + col*scale,
                    y + row*scale,
                    scale,
                    scale,
                    1
                )

def draw_big_text(text, x, y, scale=3, spacing=2):
    for i, char in enumerate(text):
        draw_big_digit(char, x + i*(5*scale + spacing), y, scale)

# --- Time update ---
def update_time():
    global hour, minute, second
    second += 1
    if second >= 60:
        second = 0
        minute += 1
    if minute >= 60:
        minute = 0
        hour += 1
    if hour >= 24:
        hour = 0

# --- Stopwatch ---
def update_stopwatch():
    global sw_time
    if sw_running:
        sw_time += 1

# --- Buttons ---
def handle_buttons():
    global mode, menu_index, set_stage
    global hour, minute, sw_running, sw_time

    if not btn_next.value():
        if mode == "menu":
            menu_index = (menu_index + 1) % len(menu_items)
        elif mode == "stopwatch":
            mode = "menu"
            menu_index = 0
        time.sleep(0.2)

    if not btn_select.value():
        if mode == "clock":
            mode = "menu"

        elif mode == "menu":
            item = menu_items[menu_index]

            if item == "Set Time":
                mode = "set_time"
                set_stage = "hour"

            elif item == "LED":
                led.value(not led.value())

            elif item == "Stopwatch":
                mode = "stopwatch"

        elif mode == "set_time":
            if set_stage == "hour":
                set_stage = "minute"
            else:
                mode = "clock"

        elif mode == "stopwatch":
            sw_time = 0

        time.sleep(0.2)

    if not btn_action.value():
        if mode == "set_time":
            if set_stage == "hour":
                hour = (hour + 1) % 24
            elif set_stage == "minute":
                minute = (minute + 1) % 60

        elif mode == "stopwatch":
            sw_running = not sw_running

        time.sleep(0.2)

# --- UI ---
def draw():
    oled.fill(0)

    if mode == "clock":
        # ONLY THIS IS BIG
        draw_big_text("{:02d}:{:02d}".format(hour, minute), 0, 2, scale=3)

    elif mode == "menu":
        oled.text("MENU", 0, 0)
        oled.text(">", 0, 16)
        oled.text(menu_items[menu_index], 10, 16)

    elif mode == "set_time":
        oled.text("SET TIME", 0, 0)

        if set_stage == "hour":
            oled.text("Hour: {:02d}".format(hour), 0, 16)
        else:
            oled.text("Min : {:02d}".format(minute), 0, 16)

    elif mode == "stopwatch":
        oled.text("STOPWATCH", 0, 0)
        oled.text("Time: {}".format(sw_time), 0, 16)

    oled.show()

# --- MAIN ---
def main():
    last_tick = time.ticks_ms()

    while True:
        handle_buttons()
        draw()

        if time.ticks_diff(time.ticks_ms(), last_tick) >= 1000:
            if mode == "clock":
                update_time()
            if mode == "stopwatch":
                update_stopwatch()

            last_tick = time.ticks_ms()

main()
