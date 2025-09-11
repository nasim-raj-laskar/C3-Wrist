# VitalEdge Project Overview

## What is VitalEdge?
A wearable health monitoring system that tracks vital signs and sends data to the cloud for analysis and visualization.

## System Components

### 1. Hardware Layer
- **ESP32**: Main microcontroller with WiFi capability
- **MAX30102**: Heart rate and SpO₂ sensor
- **MPU6050**: 6-axis accelerometer/gyroscope for activity detection
- **OLED Display**: Real-time data visualization
- **Battery**: Rechargeable Li-ion for portability

### 2. Firmware Layer
- **Arduino IDE**: Development environment
- **WiFi Connection**: Connects to internet
- **Sensor Reading**: Collects heart rate, SpO₂, and motion data
- **Data Transmission**: Sends JSON data to AWS IoT Core

### 3. Cloud Layer (AWS)
- **IoT Core**: Receives data from ESP32
- **Lambda**: Processes incoming sensor data
- **DynamoDB**: Stores health data with timestamps
- **SageMaker**: Machine learning for activity classification
- **API Gateway**: Provides REST API for dashboard

### 4. Dashboard Layer
- **HTML/CSS/JS**: Simple web interface
- **Chart.js**: Real-time data visualization
- **S3 Hosting**: Static website hosting
- **Real-time Updates**: Live health monitoring

## Data Flow
1. ESP32 reads sensors → 2. Sends to IoT Core → 3. Lambda processes → 4. Stores in DynamoDB → 5. Dashboard displays

## Key Features
- Real-time heart rate monitoring
- Blood oxygen level tracking
- Activity classification (sitting, walking, running)
- Cloud data storage and analysis
- Web-based dashboard with live charts
- Historical data trends