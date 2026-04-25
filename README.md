# C3-Wrist

A MicroPython-based wearable health monitoring device built on the ESP32-C3, featuring real-time vitals tracking on a OLED display.

<p align="center">
  <img src="assets/img1.jpg" width="45%" />
  <img src="assets/img2.jpg" width="45%" />
  
</p>

---

## Hardware

| Component | Interface | I2C Address | Pins |
|-----------|-----------|-------------|------|
| SSD1306 OLED (128×32) | I2C (hw) | `0x3C` | SCL=7, SDA=6 |
| MAX30102 HR/SpO₂ | SoftI2C | `0x57` | SCL=7, SDA=6 |
| MPU6050 IMU | I2C (hw) | `0x68` | SCL=7, SDA=6 |
| Button Next | GPIO INPUT_PULLUP | — | 21 |
| Button Select | GPIO INPUT_PULLUP | — | 20 |
| Button Action | GPIO INPUT_PULLUP | — | 10 |
| LED | GPIO OUTPUT | — | 9 |


---

## Firmware Architecture

### `firmware/main.py` — Main Application

The firmware runs a single cooperative loop at ~1-second tick resolution using `time.ticks_ms()` for non-blocking timekeeping.

**UI State Machine:**

```
clock ──(Select)──► menu ──(Select: Set Time)──► set_time
                 │                                    │
                 ├──(Select: LED)──► toggle LED       └──(Select)──► clock
                 └──(Select: Stopwatch)──► stopwatch
```

**Modes:**

| Mode | Description |
|------|-------------|
| `clock` | Big-digit HH:MM display, 1Hz tick |
| `menu` | Scrollable 3-item menu via Next button |
| `set_time` | Increment hour/minute via Action button |
| `stopwatch` | 1Hz counter; Action = start/stop, Select = reset |

**Big-digit rendering** uses a pixel-font dict of 5×7 bitmaps, scaled by a `scale` factor (default 3×) and drawn with `oled.fill_rect()`. Each character cell is `5*scale + spacing` pixels wide.

---
