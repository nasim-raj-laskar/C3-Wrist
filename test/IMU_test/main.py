from machine import I2C, Pin
import time

# =========================
# MPU6050 CONSTANTS
# =========================
MPU6050_ADDRESS = 0x68

POWER_MANAGEMENT_1 = 0x6B
ACCEL_X_HIGH = 0x3B

ACCEL_SCALE_FACTOR = 16384   # LSB per g (±2g range)
GYRO_SCALE_FACTOR = 131      # LSB per degree/second (±250 dps)

# =========================
# I2C SETUP
# =========================
i2c = I2C(
    0,
    scl=Pin(22),
    sda=Pin(21),
    freq=400000
)

# =========================
# INITIALIZE MPU6050
# =========================
def initialize_mpu6050():
    i2c.writeto_mem(
        MPU6050_ADDRESS,
        POWER_MANAGEMENT_1,
        b'\x00'
    )
    time.sleep(0.1)
    print("MPU6050 initialized")

# =========================
# READ 16-BIT SIGNED VALUE
# =========================
def read_signed_16bit(register_address):
    data = i2c.readfrom_mem(
        MPU6050_ADDRESS,
        register_address,
        2
    )

    high_byte = data[0]
    low_byte = data[1]

    value = (high_byte << 8) | low_byte

    if value > 32767:
        value = value - 65536

    return value

# =========================
# READ ALL SENSOR VALUES
# =========================
def read_mpu6050():
    accel_x = read_signed_16bit(ACCEL_X_HIGH)
    accel_y = read_signed_16bit(ACCEL_X_HIGH + 2)
    accel_z = read_signed_16bit(ACCEL_X_HIGH + 4)

    gyro_x = read_signed_16bit(ACCEL_X_HIGH + 8)
    gyro_y = read_signed_16bit(ACCEL_X_HIGH + 10)
    gyro_z = read_signed_16bit(ACCEL_X_HIGH + 12)

    return accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z

# =========================
# MAIN LOOP
# =========================
def main():
    initialize_mpu6050()
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = read_mpu6050()

            # Convert accelerometer values to g
            accel_x_g = accel_x / ACCEL_SCALE_FACTOR
            accel_y_g = accel_y / ACCEL_SCALE_FACTOR
            accel_z_g = accel_z / ACCEL_SCALE_FACTOR

            # Convert gyroscope values to degrees per second
            gyro_x_dps = gyro_x / GYRO_SCALE_FACTOR
            gyro_y_dps = gyro_y / GYRO_SCALE_FACTOR
            gyro_z_dps = gyro_z / GYRO_SCALE_FACTOR

            print(
                "ACC (g):",
                round(accel_x_g, 2),
                round(accel_y_g, 2),
                round(accel_z_g, 2),
                " | GYR (dps):",
                round(gyro_x_dps, 1),
                round(gyro_y_dps, 1),
                round(gyro_z_dps, 1)
            )

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nStopped by user")

# =========================
# PROGRAM ENTRY POINT
# =========================
if __name__ == "__main__":
    main()
