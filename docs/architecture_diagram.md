# VitalEdge System Architecture

## 📊 Visual System Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   HARDWARE      │    │     CLOUD       │    │   DASHBOARD     │
│                 │    │                 │    │                 │
│  ┌───────────┐  │    │  ┌───────────┐  │    │  ┌───────────┐  │
│  │   ESP32   │  │    │  │ IoT Core  │  │    │  │    S3     │  │
│  │           │  │    │  │           │  │    │  │ (Website) │  │
│  │ ┌───────┐ │  │    │  │ ┌───────┐ │  │    │  │           │  │
│  │ │MAX30102│ │◄─┼────┼──┤│ MQTT  ││  │    │  │ ┌───────┐ │  │
│  │ │(HR/SpO2)│ │  │    │  │ │Broker││  │    │  │ │Chart.js│ │  │
│  │ └───────┘ │  │    │  │ └───────┘│  │    │  │ │       │ │  │
│  │           │  │    │  └───────────┘  │    │  │ └───────┘ │  │
│  │ ┌───────┐ │  │    │         │       │    │  └───────────┘  │
│  │ │MPU6050│ │  │    │         ▼       │    │         ▲       │
│  │ │(Accel)│ │  │    │  ┌───────────┐  │    │         │       │
│  │ └───────┘ │  │    │  │  Lambda   │  │    │  ┌───────────┐  │
│  │           │  │    │  │(Process)  │  │    │  │API Gateway│  │
│  │ ┌───────┐ │  │    │  └─────┬─────┘  │    │  │           │  │
│  │ │ OLED  │ │  │    │        │        │    │  └─────┬─────┘  │
│  │ │Display│ │  │    │        ▼        │    │        │        │
│  │ └───────┘ │  │    │  ┌───────────┐  │    │        │        │
│  └───────────┘  │    │  │ DynamoDB  │  │    │        │        │
└─────────────────┘    │  │ (Storage) │◄─┼────────────┘        │
                       │  └───────────┘  │                     │
                       │         │       │                     │
                       │         ▼       │                     │
                       │  ┌───────────┐  │                     │
                       │  │SageMaker  │  │                     │
                       │  │(ML Model) │  │                     │
                       │  └───────────┘  │                     │
                       └─────────────────┘                     │
                                                               │
┌──────────────────────────────────────────────────────────────┘
│
▼
👤 USER ACCESS VIA WEB BROWSER
```

## 🔄 Data Flow Sequence

### 1. Sensor Reading (ESP32)
```
MAX30102 → Heart Rate + SpO₂ data
MPU6050  → Accelerometer data (X,Y,Z)
ESP32    → Combines data into JSON
```

### 2. Data Transmission
```
ESP32 → WiFi → Internet → AWS IoT Core
Topic: "health-band/data"
Format: {"timestamp": 123, "heart_rate": 75, "spo2": 98, "accel_x": 100, ...}
```

### 3. Cloud Processing
```
IoT Core → Triggers Lambda Function
Lambda   → Processes data + Adds activity classification
Lambda   → Stores in DynamoDB table
```

### 4. Data Storage Schema
```
DynamoDB Table: "health-data"
├── device_id (String) - Primary Key
├── timestamp (Number) - Sort Key  
├── heart_rate (Number)
├── spo2 (Number)
├── accel_x, accel_y, accel_z (Number)
├── activity (String) - "sitting", "walking", "running"
└── processed_at (String) - ISO timestamp
```

### 5. Dashboard Access
```
User Browser → S3 Static Website
JavaScript   → Calls API Gateway
API Gateway  → Queries DynamoDB
Chart.js     → Displays real-time graphs
```

## 🏗️ Component Responsibilities

### ESP32 Firmware
- Read sensors every 100ms
- Calculate average heart rate
- Send data via MQTT to AWS
- Display current BPM on OLED

### AWS Lambda
- Receive IoT messages
- Classify activity based on accelerometer
- Store processed data in DynamoDB
- Handle errors gracefully

### DynamoDB
- Store all sensor readings
- Enable fast queries by timestamp
- Automatically scale with usage
- Maintain data for analysis

### Web Dashboard
- Fetch latest 100 readings
- Display real-time line charts
- Show current vital signs
- Update every 5 seconds

### SageMaker (Future)
- Train ML model on collected data
- Improve activity classification
- Detect anomalies in vital signs
- Provide health insights

## 🔐 Security Considerations

### Device Security
- X.509 certificates for ESP32
- Encrypted MQTT communication
- Device-specific credentials

### Cloud Security
- IAM roles with minimal permissions
- API Gateway authentication
- VPC endpoints (if needed)
- Data encryption at rest

### Dashboard Security
- HTTPS only (S3 + CloudFront)
- API rate limiting
- Input validation
- No sensitive data in frontend