#include <Wire.h>
#include "MAX30105.h"   // SparkFun MAX3010x library
MAX30105 particleSensor;

void setup() {
  Serial.begin(115200);  // Match with Serial Plotter baud
  Wire.begin();

  if (!particleSensor.begin(Wire, I2C_SPEED_STANDARD)) {
    Serial.println("MAX30102 not found. Check wiring/power.");
    while (1);
  }

  // Configure the sensor
  particleSensor.setup(); 
  particleSensor.setPulseAmplitudeRed(0x0A);  // Red LED
  particleSensor.setPulseAmplitudeIR(0x0A);   // IR LED
}

void loop() {
  long redValue = particleSensor.getRed();
  long irValue  = particleSensor.getIR();

  // Print in CSV format for Serial Plotter
  Serial.print(redValue);
  Serial.print(",");
  Serial.println(irValue);

  delay(20); // ~50 Hz sample rate
}
