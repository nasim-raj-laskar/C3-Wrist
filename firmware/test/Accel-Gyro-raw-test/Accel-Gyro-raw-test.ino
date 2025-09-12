#include <Wire.h>
#include "MPU6050.h"

MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  Serial.println("Initializing I2C devices...");
  mpu.initialize();

  if (mpu.testConnection()) {
    Serial.println("MPU6050 connection successful!");
  } else {
    Serial.println("MPU6050 connection failed!");
  }
}

void loop() {
  int16_t ax, ay, az;
  int16_t gx, gy, gz;

  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  Serial.printf("Accel X=%d Y=%d Z=%d | Gyro X=%d Y=%d Z=%d\n", 
                 ax, ay, az, gx, gy, gz);

  delay(500);
}
