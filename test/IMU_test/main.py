from machine import I2C, Pin
import time
import ssd1306

MPU6050_ADDRESS = 0x68
POWER_MANAGEMENT_1 = 0x6B
ACCEL_X_HIGH = 0x3B

ACCEL_SCALE_FACTOR = 16384
GYRO_SCALE_FACTOR = 131

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

oled = ssd1306.SSD1306_I2C(128, 32, i2c)

def initialize_mpu6050():
    i2c.writeto_mem(MPU6050_ADDRESS, POWER_MANAGEMENT_1, b'\x00')
    time.sleep(0.1)

# READ SIGNED 16-BIT VALUE FROM REGISTER
def read_signed_16bit(register_address):
    data = i2c.readfrom_mem(MPU6050_ADDRESS, register_address, 2)
    value = (data[0] << 8) | data[1]
    if value > 32767:
        value -= 65536
    return value

# READ ALL SENSOR VALUES
def read_mpu6050():
    accel_x = read_signed_16bit(ACCEL_X_HIGH)
    accel_y = read_signed_16bit(ACCEL_X_HIGH + 2)
    accel_z = read_signed_16bit(ACCEL_X_HIGH + 4)

    gyro_x = read_signed_16bit(ACCEL_X_HIGH + 8)
    gyro_y = read_signed_16bit(ACCEL_X_HIGH + 10)
    gyro_z = read_signed_16bit(ACCEL_X_HIGH + 12)

    return accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z


def main():
    initialize_mpu6050()
    oled.fill(0)
    oled.text("MPU6050 Ready", 0, 0)
    oled.show()
    time.sleep(1)

    while True:
        ax, ay, az, gx, gy, gz = read_mpu6050()

        ax_g = ax / ACCEL_SCALE_FACTOR
        ay_g = ay / ACCEL_SCALE_FACTOR
        az_g = az / ACCEL_SCALE_FACTOR

        gx_dps = gx / GYRO_SCALE_FACTOR
        gy_dps = gy / GYRO_SCALE_FACTOR
        gz_dps = gz / GYRO_SCALE_FACTOR

        oled.fill(0)
        oled.text("ACC(g):", 0, 0)
        oled.text("X:{:.2f}".format(ax_g), 0, 10)
        oled.text("Y:{:.2f}".format(ay_g), 64, 10)
        oled.text("Z:{:.2f}".format(az_g), 0, 20)

        oled.show()
        time.sleep(0.5)

if __name__ == "__main__":
    main()
