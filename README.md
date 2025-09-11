# VitalEdge - AI-IoT Health Band

Real-time health monitoring system using ESP32, cloud ML, and web dashboard.

## 🎯 Project Overview

Wearable health band that monitors heart rate, SpO₂, and activity patterns using:
- **Hardware**: ESP32 + MAX30102 + MPU6050 + OLED
- **Cloud**: AWS IoT Core + Lambda + DynamoDB + SageMaker
- **Dashboard**: Custom web app (S3 + API Gateway)

## 🚀 Quick Start

1. **Hardware Setup**: Follow `hardware/component_list.md`
2. **Flash Firmware**: Use Arduino IDE with `firmware/src/health_band.ino`
3. **AWS Setup**: Configure IoT Core using `cloud/iot_core_setup.md`
4. **Dashboard**: Deploy web app from `dashboard/web_app/`

## 📁 Structure

- `firmware/` - ESP32 Arduino code
- `cloud/` - AWS Lambda, DynamoDB, SageMaker
- `dashboard/` - Web dashboard
- `hardware/` - Circuit diagrams, components
- `data/` - Raw/processed sensor data
- `docs/` - Documentation

## 🔧 Tech Stack

- **Firmware**: Arduino IDE (ESP32)
- **Cloud**: AWS (IoT Core, Lambda, DynamoDB, SageMaker)
- **Frontend**: HTML/JS + Chart.js
- **ML**: Python (scikit-learn/TensorFlow)

## 📊 Features

- Real-time heart rate & SpO₂ monitoring
- Activity classification (walking, running, sitting)
- Cloud data storage & ML analysis
- Web dashboard with live charts