#include <Wire.h>
#include "MAX30105.h"

MAX30105 particleSensor;

void setup() {
  Serial.begin(115200);
  delay(200);

  // Start I2C with explicit pins for ESP32
  Wire.begin(21, 22);

  Serial.println("Initializing MAX30102...");

  if (particleSensor.begin(Wire, I2C_SPEED_STANDARD) == false) {
    Serial.println("MAX30102 was not found. Please check wiring/power.");
    while (1);
  }

  // Configure sensor: default settings
  particleSensor.setup();  
  particleSensor.setPulseAmplitudeRed(0x1F);  // enable red LED
  particleSensor.setPulseAmplitudeIR(0x1F);   // enable IR LED
}

void loop() {
  Serial.print(" R[");
  Serial.print(particleSensor.getRed());
  Serial.print("] IR[");
  Serial.print(particleSensor.getIR());
  Serial.println("]");

  delay(200);  // slow down output a bit
}
