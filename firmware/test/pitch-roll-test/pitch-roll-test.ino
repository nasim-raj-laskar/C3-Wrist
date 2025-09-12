#include <Wire.h>
#include <math.h>

const uint8_t MPU = 0x68;   // I2C address (scanner found 0x68)
const int CAL_SAMPLES = 600; // number of samples for calibration (increase for better bias)

// scale factors (default device ranges)
// If you changed sensor range, update these accordingly
const float ACCEL_SCALE = 16384.0; // LSB per g at ±2g
const float GYRO_SCALE  = 131.0;   // LSB per °/s at ±250°/s

// calibration offsets (raw)
long ax_off = 0, ay_off = 0, az_off = 0;
long gx_off = 0, gy_off = 0, gz_off = 0;

void writeRegister(uint8_t reg, uint8_t val) {
  Wire.beginTransmission(MPU);
  Wire.write(reg);
  Wire.write(val);
  Wire.endTransmission(true);
}

int16_t read16(uint8_t reg) {
  Wire.beginTransmission(MPU);
  Wire.write(reg);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, (uint8_t)2, (uint8_t)true);
  int16_t hi = Wire.read();
  int16_t lo = Wire.read();
  return (hi << 8) | lo;
}

void calibrateOffsets() {
  Serial.println("Calibrating... keep the board stationary and flat.");
  long sax = 0, say = 0, saz = 0, sgx = 0, sgy = 0, sgz = 0;
  for (int i = 0; i < CAL_SAMPLES; ++i) {
    int16_t AcX = read16(0x3B);
    int16_t AcY = read16(0x3D);
    int16_t AcZ = read16(0x3F);
    int16_t GyX = read16(0x43);
    int16_t GyY = read16(0x45);
    int16_t GyZ = read16(0x47);

    sax += AcX; say += AcY; saz += AcZ;
    sgx += GyX; sgy += GyY; sgz += GyZ;
    delay(3); // small spacing
  }
  ax_off = sax / CAL_SAMPLES;
  ay_off = say / CAL_SAMPLES;
  az_off = saz / CAL_SAMPLES;
  gx_off = sgx / CAL_SAMPLES;
  gy_off = sgy / CAL_SAMPLES;
  gz_off = sgz / CAL_SAMPLES;

  // For accel Z we expect ~+1g on Z when flat — adjust az_off to represent 1g
  // If you want az_off to be the zero-g baseline (for subtracting), do:
  // az_off -= ACCEL_SCALE;  // uncomment if you want az_off to be zero when gravity removed
  // But in our code below we'll convert and then subtract 1g from Az when computing angles.

  Serial.println("Calibration done.");
  Serial.printf("Raw offsets: ax=%ld ay=%ld az=%ld | gx=%ld gy=%ld gz=%ld\n",
                ax_off, ay_off, az_off, gx_off, gy_off, gz_off);
}

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22, 100000); // SDA=21, SCL=22, set 100kHz (more reliable)
  delay(500);

  // Wake up device
  writeRegister(0x6B, 0x00); // PWR_MGMT_1 = 0 (wake up)
  delay(100);

  // Optional: set accel/gyro ranges explicitly if module supports it
  // writeRegister(0x1C, 0x00); // ACCEL_CONFIG = 0 (±2g)
  // writeRegister(0x1B, 0x00); // GYRO_CONFIG  = 0 (±250°/s)
  // delay(20);

  // Quick WHO_AM_I read for info (non-fatal)
  Wire.beginTransmission(MPU);
  Wire.write(0x75);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, (uint8_t)1, (uint8_t)true);
  if (Wire.available()) {
    uint8_t id = Wire.read();
    Serial.printf("WHO_AM_I = 0x%02X\n", id);
  }

  calibrateOffsets();
}

void loop() {
  // read 14 bytes from 0x3B -> accel(6) temp(2) gyro(6)
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, (uint8_t)14, (uint8_t)true);

  int16_t AcX = Wire.read() << 8 | Wire.read();
  int16_t AcY = Wire.read() << 8 | Wire.read();
  int16_t AcZ = Wire.read() << 8 | Wire.read();
  int16_t Tmp = Wire.read() << 8 | Wire.read();
  int16_t GyX = Wire.read() << 8 | Wire.read();
  int16_t GyY = Wire.read() << 8 | Wire.read();
  int16_t GyZ = Wire.read() << 8 | Wire.read();

  // subtract raw offsets
  float rawAx = (float)(AcX - ax_off);
  float rawAy = (float)(AcY - ay_off);
  float rawAz = (float)(AcZ - az_off);

  float rawGx = (float)(GyX - gx_off);
  float rawGy = (float)(GyY - gy_off);
  float rawGz = (float)(GyZ - gz_off);

  // convert to physical units
  float Ax_g = rawAx / ACCEL_SCALE;    // in g
  float Ay_g = rawAy / ACCEL_SCALE;
  float Az_g = rawAz / ACCEL_SCALE;

  float Gx_dps = rawGx / GYRO_SCALE;   // in degrees per second
  float Gy_dps = rawGy / GYRO_SCALE;
  float Gz_dps = rawGz / GYRO_SCALE;

  // Compute pitch & roll from accelerometer (degrees)
  float pitch = atan2(Ay_g, sqrt(Ax_g*Ax_g + Az_g*Az_g)) * 180.0 / M_PI;
  float roll  = atan2(-Ax_g, Az_g) * 180.0 / M_PI;

  // Temperature conversion (MPU raw -> °C)
  float temperature = (Tmp / 340.0) + 36.53;

  Serial.printf("A[g] X=%.3f Y=%.3f Z=%.3f | G[°/s] X=%.2f Y=%.2f Z=%.2f | T=%.2f°C\n",
                Ax_g, Ay_g, Az_g, Gx_dps, Gy_dps, Gz_dps, temperature);
  Serial.printf("Pitch=%.2f°, Roll=%.2f°\n\n", pitch, roll);

  delay(1000);
}
