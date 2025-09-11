# API Gateway Setup for VitalEdge Dashboard

## 🎯 Overview
Create REST API to serve health data from DynamoDB to your web dashboard.

## 📋 Prerequisites
- DynamoDB table with health data
- Basic understanding of REST APIs
- AWS Console access

## 🚀 Step-by-Step Setup

### Step 1: Create REST API
1. **Go to API Gateway Console**
   - Search "API Gateway" in AWS Console
   - Click "Create API"

2. **Choose API Type**
   - Select "REST API" (not private)
   - Click "Build"

3. **API Configuration**
   - API name: `health-band-api`
   - Description: `API for VitalEdge health data`
   - Endpoint Type: Regional
   - Click "Create API"

### Step 2: Create Resources & Methods

#### Resource: /health-data
1. **Create Resource**
   - Click "Actions" → "Create Resource"
   - Resource Name: `health-data`
   - Resource Path: `/health-data`
   - Enable CORS: ✓
   - Click "Create Resource"

2. **Create GET Method**
   - Select `/health-data` resource
   - Click "Actions" → "Create Method"
   - Choose "GET" from dropdown
   - Click checkmark

#### Resource: /latest
1. **Create Nested Resource**
   - Select `/health-data` resource
   - Click "Actions" → "Create Resource"
   - Resource Name: `latest`
   - Resource Path: `/latest`
   - Click "Create Resource"

2. **Create GET Method for Latest**
   - Select `/health-data/latest` resource
   - Click "Actions" → "Create Method"
   - Choose "GET"

### Step 3: Configure Lambda Integration

#### Create Lambda Function First
```python
import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('health-data')

def lambda_handler(event, context):
    try:
        # Get query parameters
        limit = int(event.get('queryStringParameters', {}).get('limit', 100))
        device_id = event.get('queryStringParameters', {}).get('device_id', 'health-band-device-01')
        
        # Query DynamoDB
        response = table.query(
            KeyConditionExpression=Key('device_id').eq(device_id),
            ScanIndexForward=False,  # Sort by timestamp descending
            Limit=limit
        )
        
        # Convert Decimal to float for JSON serialization
        items = []
        for item in response['Items']:
            converted_item = {}
            for key, value in item.items():
                if isinstance(value, Decimal):
                    converted_item[key] = float(value)
                else:
                    converted_item[key] = value
            items.append(converted_item)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET,OPTIONS'
            },
            'body': json.dumps({
                'data': items,
                'count': len(items)
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }
```

#### Configure API Gateway Integration
1. **Setup Integration**
   - Integration type: Lambda Function
   - Use Lambda Proxy integration: ✓
   - Lambda Region: (your region)
   - Lambda Function: `health-data-api`
   - Click "Save"

2. **Grant Permissions**
   - Click "OK" when prompted to give API Gateway permission

### Step 4: Enable CORS

#### For /health-data Resource
1. **Select Resource**
   - Click on `/health-data` resource
   - Click "Actions" → "Enable CORS"

2. **CORS Configuration**
   ```
   Access-Control-Allow-Origin: *
   Access-Control-Allow-Headers: Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token
   Access-Control-Allow-Methods: GET,OPTIONS
   ```
   - Click "Enable CORS and replace existing CORS headers"

#### Repeat for /latest Resource

### Step 5: Deploy API
1. **Create Deployment**
   - Click "Actions" → "Deploy API"
   - Deployment stage: New Stage
   - Stage name: `prod`
   - Stage description: `Production stage`
   - Click "Deploy"

2. **Get API URL**
   - Copy the "Invoke URL"
   - Format: `https://xxxxxxxxxx.execute-api.region.amazonaws.com/prod`

## 🧪 Testing Your API

### Test Endpoints

#### Get All Health Data
```bash
curl "https://your-api-id.execute-api.region.amazonaws.com/prod/health-data"
```

#### Get Latest 10 Records
```bash
curl "https://your-api-id.execute-api.region.amazonaws.com/prod/health-data?limit=10"
```

#### Get Specific Device Data
```bash
curl "https://your-api-id.execute-api.region.amazonaws.com/prod/health-data?device_id=health-band-device-01&limit=50"
```

### Expected Response Format
```json
{
  "data": [
    {
      "device_id": "health-band-device-01",
      "timestamp": 1640995200000,
      "heart_rate": 75,
      "spo2": 98,
      "accel_x": 1024,
      "accel_y": -512,
      "accel_z": 2048,
      "activity": "walking",
      "processed_at": "2021-12-31T12:00:00Z"
    }
  ],
  "count": 1
}
```

## 🌐 Frontend Integration

### JavaScript Fetch Example
```javascript
// Fetch latest health data
async function fetchHealthData(limit = 100) {
    try {
        const response = await fetch(
            `https://your-api-id.execute-api.region.amazonaws.com/prod/health-data?limit=${limit}`
        );
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data.data; // Return the health records array
        
    } catch (error) {
        console.error('Error fetching health data:', error);
        return [];
    }
}

// Usage in dashboard
fetchHealthData(50).then(data => {
    updateCharts(data);
    displayCurrentVitals(data[0]); // Most recent reading
});
```

### Chart.js Integration
```javascript
// Update heart rate chart
function updateHeartRateChart(healthData) {
    const labels = healthData.map(item => 
        new Date(item.timestamp).toLocaleTimeString()
    );
    const heartRates = healthData.map(item => item.heart_rate);
    
    heartRateChart.data.labels = labels;
    heartRateChart.data.datasets[0].data = heartRates;
    heartRateChart.update();
}
```

## 🔐 Security Enhancements

### API Key Authentication
1. **Create API Key**
   - Go to "API Keys" in API Gateway
   - Click "Actions" → "Create API Key"
   - Name: `dashboard-key`
   - Click "Save"

2. **Create Usage Plan**
   - Go to "Usage Plans"
   - Click "Create"
   - Name: `dashboard-plan`
   - Throttle: 1000 requests/second
   - Quota: 10000 requests/month

3. **Associate API Key**
   - Add API key to usage plan
   - Add API stage to usage plan

### Request Validation
```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "limit": {
      "type": "string",
      "pattern": "^[1-9][0-9]*$"
    },
    "device_id": {
      "type": "string",
      "minLength": 1,
      "maxLength": 50
    }
  }
}
```

## 📊 Monitoring & Analytics

### CloudWatch Metrics
- API Gateway calls
- Lambda execution duration
- Error rates
- Cache hit/miss ratios

### Custom Metrics
```python
import boto3
cloudwatch = boto3.client('cloudwatch')

# Track API usage
cloudwatch.put_metric_data(
    Namespace='VitalEdge/API',
    MetricData=[
        {
            'MetricName': 'HealthDataRequests',
            'Value': 1,
            'Unit': 'Count'
        }
    ]
)
```

## 💰 Cost Optimization

### Caching Strategy
1. **Enable Caching**
   - Go to API Gateway stage
   - Enable caching for GET methods
   - Cache TTL: 300 seconds (5 minutes)

2. **Cache Key Parameters**
   - Include `limit` and `device_id` in cache key
   - Reduces DynamoDB read costs

### Request Throttling
- Set reasonable throttle limits
- Prevent abuse and control costs
- Monitor usage patterns

## 🛠️ Troubleshooting

### Common Issues

#### CORS Errors
```
Error: Access to fetch blocked by CORS policy
Solution: Ensure CORS is enabled and OPTIONS method exists
```

#### Lambda Timeout
```
Error: Task timed out after 3.00 seconds
Solution: Increase Lambda timeout or optimize DynamoDB queries
```

#### DynamoDB Throttling
```
Error: ProvisionedThroughputExceededException
Solution: Use on-demand billing or increase provisioned capacity
```

### Debug Steps
1. **Check API Gateway Logs**
   - Enable CloudWatch logging
   - Review execution logs

2. **Test Lambda Directly**
   - Use Lambda console test feature
   - Verify function works independently

3. **Monitor CloudWatch Metrics**
   - Track error rates
   - Monitor response times

## 🔄 Next Steps

After API Gateway setup:
1. **Create S3 static website** for dashboard hosting
2. **Implement real-time updates** using WebSockets
3. **Add authentication** for production use
4. **Set up monitoring alerts** for API health

## 📚 Additional Resources

- [API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/)
- [Lambda Integration Patterns](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-integrations.html)
- [CORS Configuration](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors.html)