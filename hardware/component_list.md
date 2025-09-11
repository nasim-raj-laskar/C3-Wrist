# VitalEdge Hardware Components

## 🛒 Shopping List

### Core Components
| Component | Quantity | Price (USD) | Purpose |
|-----------|----------|-------------|---------|
| ESP32 DevKit | 1 | $8-12 | Main microcontroller with WiFi |
| MAX30102 Sensor | 1 | $5-8 | Heart rate & SpO₂ measurement |
| MPU6050 Module | 1 | $3-5 | 6-axis accelerometer/gyroscope |
| 0.96" OLED Display | 1 | $4-6 | Real-time data display |
| Breadboard | 1 | $3-5 | Prototyping connections |
| Jumper Wires | 1 pack | $3-5 | Male-to-male connections |

### Power & Connectivity
| Component | Quantity | Price (USD) | Purpose |
|-----------|----------|-------------|---------|
| 3.7V Li-ion Battery | 1 | $5-8 | Portable power (optional) |
| Battery Holder | 1 | $2-3 | Secure battery mounting |
| Micro USB Cable | 1 | $3-5 | Programming & charging |

### Assembly Materials
| Component | Quantity | Price (USD) | Purpose |
|-----------|----------|-------------|---------|
| Resistors (10kΩ) | 2 | $1 | Pull-up resistors for I2C |
| Capacitors (100µF) | 2 | $1 | Power filtering |
| PCB (optional) | 1 | $5-10 | Permanent assembly |

**Total Estimated Cost: $40-70**

## 🔌 Pin Connections

### ESP32 to MAX30102 (Heart Rate Sensor)
```
ESP32    →    MAX30102
3.3V     →    VIN
GND      →    GND
GPIO21   →    SDA
GPIO22   →    SCL
```

### ESP32 to MPU6050 (Accelerometer)
```
ESP32    →    MPU6050
3.3V     →    VCC
GND      →    GND
GPIO21   →    SDA (shared with MAX30102)
GPIO22   →    SCL (shared with MAX30102)
```

### ESP32 to OLED Display
```
ESP32    →    OLED
3.3V     →    VCC
GND      →    GND
GPIO21   →    SDA (shared I2C bus)
GPIO22   →    SCL (shared I2C bus)
```

## 📐 Circuit Diagram Description

```
                    ESP32 DevKit
                   ┌─────────────┐
                   │             │
                   │    GPIO21   ├──┐ (SDA - I2C Data)
                   │    GPIO22   ├──┼─┐ (SCL - I2C Clock)
                   │             │  │ │
                   │    3.3V     ├──┼─┼─┐ (Power)
                   │    GND      ├──┼─┼─┼─┐ (Ground)
                   └─────────────┘  │ │ │ │
                                    │ │ │ │
        ┌───────────────────────────┘ │ │ │
        │ ┌─────────────────────────────┘ │ │
        │ │ ┌───────────────────────────────┘ │
        │ │ │ ┌─────────────────────────────────┘
        │ │ │ │
        ▼ ▼ ▼ ▼
   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
   │  MAX30102   │  │   MPU6050   │  │ OLED Display│
   │             │  │             │  │             │
   │ SDA  SCL    │  │ SDA  SCL    │  │ SDA  SCL    │
   │ VIN  GND    │  │ VCC  GND    │  │ VCC  GND    │
   └─────────────┘  └─────────────┘  └─────────────┘
```

## 🔧 Assembly Instructions

### Step 1: Prepare Breadboard
1. Place ESP32 on breadboard
2. Connect power rails (3.3V and GND)
3. Add pull-up resistors (10kΩ) on SDA and SCL lines

### Step 2: Connect Sensors
1. **MAX30102**: Connect to I2C bus (pins 21, 22)
2. **MPU6050**: Share same I2C bus
3. **OLED**: Also on shared I2C bus
4. Verify all connections with multimeter

### Step 3: Power Setup
1. Connect USB cable for initial testing
2. Add battery holder for portable operation
3. Test power consumption (should be <100mA)

### Step 4: Testing
1. Upload test sketch to verify each sensor
2. Check I2C addresses using scanner sketch
3. Verify OLED display shows data

## 📊 I2C Address Reference

| Device | I2C Address | Notes |
|--------|-------------|-------|
| MAX30102 | 0x57 | Heart rate sensor |
| MPU6050 | 0x68 | Accelerometer (default) |
| OLED SSD1306 | 0x3C | Display (common address) |

## ⚡ Power Consumption

| Component | Current Draw | Notes |
|-----------|--------------|-------|
| ESP32 (active) | 80mA | During WiFi transmission |
| ESP32 (sleep) | 10µA | Deep sleep mode |
| MAX30102 | 1.8mA | Continuous monitoring |
| MPU6050 | 3.9mA | Normal operation |
| OLED Display | 20mA | Full brightness |
| **Total Active** | **~105mA** | All components running |

**Battery Life Calculation**:
- 1000mAh battery ÷ 105mA = ~9.5 hours continuous operation
- With sleep optimization: 24+ hours

## 🛡️ Safety Considerations

### Electrical Safety
- Use 3.3V logic levels only
- Add fuses for battery protection
- Avoid short circuits on power rails
- Use proper gauge wires for current

### Sensor Safety
- MAX30102 uses infrared light (safe for skin contact)
- Keep sensors clean for accurate readings
- Avoid water damage to electronics
- Secure all connections to prevent disconnection

## 🔍 Troubleshooting Common Issues

### Sensor Not Detected
1. Check I2C wiring (SDA/SCL)
2. Verify power connections (3.3V/GND)
3. Run I2C scanner to find addresses
4. Check for loose connections

### Inaccurate Readings
1. Ensure good skin contact for MAX30102
2. Calibrate accelerometer on flat surface
3. Check for electromagnetic interference
4. Verify sensor orientation

### Power Issues
1. Measure voltage at sensor pins
2. Check current draw with multimeter
3. Ensure adequate power supply capacity
4. Look for voltage drops in wiring

## 📦 Recommended Suppliers

### Online Retailers
- **Amazon**: Fast shipping, good for prototyping
- **AliExpress**: Cheaper prices, longer shipping
- **Adafruit**: High quality, good documentation
- **SparkFun**: Educational resources included

### Local Options
- Electronics hobby stores
- University bookstores
- Maker spaces (may have components available)