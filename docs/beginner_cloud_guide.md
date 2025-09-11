# Beginner's Guide to AWS Cloud Setup

## 🎯 Step-by-Step Cloud Journey (New to Cloud)

### Phase 1: AWS Account Setup (Day 1)
1. **Create AWS Account**: Sign up at aws.amazon.com
2. **Enable Free Tier**: Most services we'll use are free for 12 months
3. **Install AWS CLI**: Download from AWS website
4. **Create IAM User**: Don't use root account for development

### Phase 2: IoT Core Setup (Day 2-3)
1. **Go to AWS IoT Core Console**
2. **Create a "Thing"**: This represents your ESP32 device
3. **Download Certificates**: You'll get 3 files (certificate, private key, root CA)
4. **Create IoT Policy**: Allows your device to publish/subscribe to topics
5. **Test Connection**: Use AWS IoT Test Client

### Phase 3: Database Setup (Day 4)
1. **Go to DynamoDB Console**
2. **Create Table**: Name it "health-data"
3. **Set Primary Key**: Use "device_id" and "timestamp"
4. **Configure Auto-scaling**: Keep it simple, use on-demand billing

### Phase 4: Data Processing (Day 5-6)
1. **Go to Lambda Console**
2. **Create Function**: Choose Python 3.9 runtime
3. **Set Trigger**: Connect to IoT Core topic
4. **Write Simple Code**: Process sensor data and save to DynamoDB
5. **Test Function**: Use sample JSON data

### Phase 5: API & Dashboard (Day 7-8)
1. **Create API Gateway**: REST API to read data from DynamoDB
2. **Create S3 Bucket**: Host your web dashboard
3. **Upload HTML/CSS/JS**: Simple dashboard with charts
4. **Enable Static Website**: Make your dashboard accessible

## 🚀 Visual Learning Resources

### Recommended YouTube Tutorials:
- "AWS IoT Core Tutorial for Beginners"
- "DynamoDB Basics in 10 Minutes"
- "Lambda Functions Explained Simply"
- "S3 Static Website Hosting"

### AWS Documentation:
- AWS IoT Device SDK for Arduino
- DynamoDB Getting Started Guide
- Lambda Developer Guide

## 💡 Pro Tips for Beginners

1. **Start Small**: Get one sensor working before adding others
2. **Use AWS Free Tier**: Most of this project fits in free limits
3. **Test Each Step**: Don't move to next phase until current works
4. **Save Credentials Safely**: Never commit AWS keys to GitHub
5. **Monitor Costs**: Set up billing alerts (should be $0-5/month)

## 🔧 Tools You'll Need

- **AWS Console**: Web interface for all services
- **Arduino IDE**: For ESP32 programming
- **Text Editor**: VS Code recommended for web dashboard
- **Postman**: For testing API endpoints (optional)

## 📊 Expected Timeline

- **Week 1**: Hardware assembly + basic ESP32 code
- **Week 2**: AWS setup + IoT Core connection
- **Week 3**: Data processing + storage
- **Week 4**: Dashboard + ML model (basic)

## 🆘 When You Get Stuck

1. **AWS Documentation**: Very detailed but can be overwhelming
2. **Stack Overflow**: Search for specific error messages
3. **AWS Forums**: Community help for AWS-specific issues
4. **YouTube**: Visual tutorials often help more than text