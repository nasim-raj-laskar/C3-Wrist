# AWS IoT Core Setup Guide

## 🎯 Overview
This guide walks you through setting up AWS IoT Core to receive data from your ESP32 health band.

## 📋 Prerequisites
- AWS Account (free tier eligible)
- ESP32 with WiFi capability
- Basic understanding of MQTT protocol

## 🚀 Step-by-Step Setup

### Step 1: Create IoT Thing
1. **Login to AWS Console**
   - Go to [AWS Console](https://console.aws.amazon.com)
   - Search for "IoT Core" in services

2. **Navigate to Things**
   - Click "Manage" → "Things"
   - Click "Create things"

3. **Create Single Thing**
   - Choose "Create single thing"
   - Thing name: `health-band-device-01`
   - Thing type: Leave blank (optional)
   - Click "Next"

### Step 2: Generate Device Certificate
1. **Auto-generate Certificate**
   - Select "Auto-generate a new certificate"
   - Click "Next"

2. **Download Certificates**
   - Download all 4 files:
     - `device-certificate.pem.crt`
     - `private.pem.key`
     - `public.pem.key`
     - `AmazonRootCA1.pem`
   - Store securely (never commit to GitHub!)

### Step 3: Create IoT Policy
1. **Create Policy**
   - Go to "Secure" → "Policies"
   - Click "Create policy"

2. **Policy Configuration**
   - Policy name: `HealthBandPolicy`
   - Policy document:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "iot:Connect",
           "iot:Publish",
           "iot:Subscribe",
           "iot:Receive"
         ],
         "Resource": [
           "arn:aws:iot:*:*:client/health-band-*",
           "arn:aws:iot:*:*:topic/health-band/*",
           "arn:aws:iot:*:*:topicfilter/health-band/*"
         ]
       }
     ]
   }
   ```

### Step 4: Attach Policy to Certificate
1. **Go to Certificates**
   - Navigate to "Secure" → "Certificates"
   - Find your certificate and click on it

2. **Attach Policy**
   - Click "Actions" → "Attach policy"
   - Select `HealthBandPolicy`
   - Click "Attach"

3. **Attach Thing**
   - Click "Actions" → "Attach thing"
   - Select `health-band-device-01`
   - Click "Attach"

### Step 5: Get IoT Endpoint
1. **Find Endpoint**
   - Go to "Settings" in IoT Core
   - Copy "Device data endpoint"
   - Format: `xxxxxxxxxx-ats.iot.region.amazonaws.com`

## 🔧 ESP32 Configuration

### Required Libraries
Install these libraries in Arduino IDE:
```
- WiFiClientSecure
- PubSubClient
- ArduinoJson
```

### Certificate Setup
1. **Convert Certificates to C Headers**
   - Use online converter or create manually
   - Include in ESP32 sketch as const char arrays

2. **Example Certificate Format**
   ```cpp
   const char* root_ca = \
   "-----BEGIN CERTIFICATE-----\n" \
   "MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF\n" \
   // ... rest of certificate
   "-----END CERTIFICATE-----\n";
   ```

### MQTT Topics Structure
```
health-band/data          → Sensor data publishing
health-band/status        → Device status updates
health-band/commands      → Receive commands (future)
```

## 🧪 Testing Connection

### Step 1: Use AWS IoT Test Client
1. **Go to Test Client**
   - Navigate to "Test" in IoT Core console
   - Click "MQTT test client"

2. **Subscribe to Topic**
   - Topic filter: `health-band/data`
   - Click "Subscribe"

### Step 2: Test ESP32 Connection
1. **Upload Test Sketch**
   ```cpp
   // Basic connection test
   void setup() {
     // WiFi and MQTT setup
     client.publish("health-band/data", "Hello from ESP32!");
   }
   ```

2. **Verify Message Reception**
   - Check AWS IoT Test Client
   - Should see "Hello from ESP32!" message

## 📊 Data Format Specification

### Sensor Data Message
```json
{
  "device_id": "health-band-device-01",
  "timestamp": 1640995200000,
  "heart_rate": 75,
  "spo2": 98,
  "accel_x": 1024,
  "accel_y": -512,
  "accel_z": 2048,
  "battery_level": 85,
  "firmware_version": "1.0.0"
}
```

### Status Message
```json
{
  "device_id": "health-band-device-01",
  "status": "online",
  "last_seen": 1640995200000,
  "wifi_rssi": -45,
  "free_memory": 234567
}
```

## 🔐 Security Best Practices

### Certificate Management
- Store certificates in secure location
- Use different certificates for each device
- Rotate certificates annually
- Never hardcode certificates in source code

### Policy Restrictions
- Use least privilege principle
- Restrict to specific topics
- Limit client ID patterns
- Regular policy audits

### Network Security
- Use TLS 1.2 or higher
- Verify server certificates
- Implement certificate pinning
- Monitor for unusual traffic

## 📈 Monitoring & Logging

### CloudWatch Metrics
- Connection attempts
- Message publish/subscribe rates
- Error rates
- Device registry changes

### Useful Metrics to Track
```
AWS/IoT/Connect.Success
AWS/IoT/Publish.In
AWS/IoT/Subscribe.Success
AWS/IoT/RulesExecuted
```

### Setting Up Alarms
1. Go to CloudWatch console
2. Create alarm for connection failures
3. Set SNS notification for alerts

## 🛠️ Troubleshooting

### Common Connection Issues

#### Certificate Problems
```
Error: SSL connection failed
Solution: Verify certificate format and validity
```

#### Policy Issues
```
Error: Not authorized to publish
Solution: Check policy permissions and attachment
```

#### Network Issues
```
Error: Connection timeout
Solution: Check WiFi, firewall, and endpoint URL
```

### Debug Steps
1. **Check Certificate Expiry**
   ```bash
   openssl x509 -in certificate.pem -text -noout
   ```

2. **Verify Policy JSON**
   - Use AWS Policy Simulator
   - Test specific actions

3. **Monitor CloudWatch Logs**
   - Enable IoT Core logging
   - Check for error messages

## 💰 Cost Considerations

### Free Tier Limits (12 months)
- 2.25 million messages per month
- 225,000 registry operations
- 250,000 device shadows operations

### Typical Usage Estimate
- 1 message every 10 seconds = 8,640 messages/day
- Monthly usage: ~260,000 messages
- **Result**: Stays within free tier limits

### Cost After Free Tier
- $1.20 per million messages
- Estimated monthly cost: $0.31

## 🔄 Next Steps

After successful IoT Core setup:
1. **Set up Lambda function** to process incoming data
2. **Configure DynamoDB** for data storage
3. **Create IoT Rules** for message routing
4. **Implement device shadows** for configuration management

## 📚 Additional Resources

- [AWS IoT Device SDK for Arduino](https://github.com/aws/aws-iot-device-sdk-arduino-yun)
- [IoT Core Developer Guide](https://docs.aws.amazon.com/iot/latest/developerguide/)
- [MQTT Protocol Specification](http://mqtt.org/)