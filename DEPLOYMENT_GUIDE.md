# Deployment Guide

## Production Deployment Checklist

### Pre-Deployment
- [ ] All tests pass (>80% coverage)
- [ ] Code reviewed and approved
- [ ] Security audit completed
- [ ] Documentation updated
- [ ] Performance benchmarks meet targets
- [ ] Database migrations tested
- [ ] Environment variables configured
- [ ] SSL/TLS certificates valid
- [ ] Monitoring alerts setup
- [ ] Backup strategy implemented

### Docker Deployment

#### Building Docker Image

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Run application
CMD ["python", "app.py"]
```

#### Build and Run

```bash
# Build image
docker build -t truck-detector:latest .

# Test locally
docker run -p 5000:5000 truck-detector:latest

# Push to registry
docker tag truck-detector:latest myregistry.azurecr.io/truck-detector:latest
docker push myregistry.azurecr.io/truck-detector:latest
```

### Kubernetes Deployment

#### Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: truck-detector
spec:
  replicas: 3
  selector:
    matchLabels:
      app: truck-detector
  template:
    metadata:
      labels:
        app: truck-detector
    spec:
      containers:
      - name: truck-detector
        image: myregistry.azurecr.io/truck-detector:latest
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
            nvidia.com/gpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2000m"
            nvidia.com/gpu: "1"
        env:
        - name: CONFIDENCE_THRESHOLD
          value: "0.5"
        - name: MODEL_PATH
          value: "/models/detector_model.pb"
        volumeMounts:
        - name: models
          mountPath: /models
      volumes:
      - name: models
        configMap:
          name: models-config
---
apiVersion: v1
kind: Service
metadata:
  name: truck-detector-service
spec:
  selector:
    app: truck-detector
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
```

#### Deploy to Kubernetes

```bash
# Deploy
kubectl apply -f deployment.yaml

# Check status
kubectl get pods
kubectl get service truck-detector-service

# View logs
kubectl logs -f deployment/truck-detector

# Scale deployment
kubectl scale deployment truck-detector --replicas=5
```

### AWS ECS Deployment

```bash
# Create ECR repository
aws ecr create-repository --repository-name truck-detector

# Push image
docker tag truck-detector:latest <aws-account>.dkr.ecr.us-east-1.amazonaws.com/truck-detector:latest
aws ecr get-login-password | docker login --username AWS --password-stdin <aws-account>.dkr.ecr.us-east-1.amazonaws.com
docker push <aws-account>.dkr.ecr.us-east-1.amazonaws.com/truck-detector:latest

# Create ECS task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service --cluster truck-detection-cluster --service-name truck-detector --task-definition truck-detector:1 --desired-count 3
```

### Azure App Service Deployment

```bash
# Create resource group
az group create --name truck-detector-rg --location eastus

# Create container registry
az acr create --resource-group truck-detector-rg --name myregistry --sku Basic

# Build image
az acr build --registry myregistry --image truck-detector:latest .

# Create App Service plan
az appservice plan create --name truck-detector-plan --resource-group truck-detector-rg --sku P1V2 --is-linux

# Create web app
az webapp create --resource-group truck-detector-rg --plan truck-detector-plan --name truck-detector-app --deployment-container-image-name-user truck-detector:latest
```

## Monitoring & Logging

### Application Metrics

```python
from prometheus_client import Counter, Histogram
import time

detection_count = Counter('detections_total', 'Total detections')
detection_time = Histogram('detection_duration_seconds', 'Detection time')

@detection_time.time()
def detect_trucks(video_path):
    # Detection logic
    detection_count.inc()
```

### Log Aggregation

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module
        })

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger(__name__)
logger.addHandler(handler)
```

### Alerting

```yaml
# Prometheus alert configuration
groups:
- name: truck_detector
  rules:
  - alert: HighDetectionLatency
    expr: detection_duration_seconds > 1.0
    for: 5m
    annotations:
      summary: "Detection latency exceeds 1 second"
  
  - alert: HighErrorRate
    expr: rate(errors_total[5m]) > 0.05
    for: 10m
    annotations:
      summary: "Error rate > 5%"
```

## Scaling

### Horizontal Scaling

```bash
# Auto-scale based on CPU
kubectl autoscale deployment truck-detector --min=2 --max=10 --cpu-percent=70

# AWS Auto Scaling
aws autoscaling create-auto-scaling-group \
    --auto-scaling-group-name truck-detector-asg \
    --launch-template LaunchTemplateName=truck-detector \
    --min-size 2 --max-size 10 --desired-capacity 3
```

### Load Balancing

```bash
# NGINX Load Balancer
upstream truck_detector {
    server detector1:5000;
    server detector2:5000;
    server detector3:5000;
}

server {
    listen 80;
    location / {
        proxy_pass http://truck_detector;
        proxy_set_header Host $host;
    }
}
```

## Backup & Recovery

### Database Backup

```bash
# Daily backup to S3
aws s3 sync /data/models s3://bucket/backups/models --delete

# Restore
aws s3 sync s3://bucket/backups/models /data/models
```

### Disaster Recovery Plan

1. **RTO (Recovery Time Objective)**: 1 hour
2. **RPO (Recovery Point Objective)**: 15 minutes
3. **Backup Frequency**: Every 4 hours
4. **Test Schedule**: Monthly DR drills

## Security

### SSL/TLS Configuration

```python
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
import ssl

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["trusted-domain.com"]}})

# SSL context
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_context.load_cert_chain('cert.pem', 'key.pem')

# Run with SSL
app.run(ssl_context=ssl_context, host='0.0.0.0', port=443)
```

### Secret Management

```bash
# Store secrets in environment variables
export DATABASE_URL="postgresql://user:pass@host:5432/db"
export API_KEY="your-secret-key"

# Or use HashiCorp Vault
vault kv put secret/truck-detector db_password=xxxx api_key=xxxx
```

## Rollback Procedures

```bash
# Kubernetes rollback
kubectl rollout history deployment/truck-detector
kubectl rollout undo deployment/truck-detector

# Docker rollback
docker service update --image myregistry.azurecr.io/truck-detector:previous truck-detector
```

## Performance Tuning

### Database Optimization

```sql
-- Create indexes
CREATE INDEX idx_detection_timestamp ON detections(timestamp);
CREATE INDEX idx_frame_video_id ON frames(video_id);

-- Query analysis
EXPLAIN ANALYZE SELECT * FROM detections WHERE timestamp > NOW() - INTERVAL 1 DAY;
```

### Cache Configuration

```python
from functools import lru_cache
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@lru_cache(maxsize=128)
def get_model(model_id):
    cached = redis_client.get(f"model:{model_id}")
    if cached:
        return pickle.loads(cached)
    # Load from disk
```

## Testing in Production

### Canary Deployment

```bash
# Deploy to 10% of traffic
kubectl set image deployment/truck-detector \
    truck-detector=myregistry.azurecr.io/truck-detector:new \
    --record

# Monitor metrics - if healthy, scale up
kubectl scale deployment truck-detector --replicas=10
```

### A/B Testing

```python
import random

@app.route('/detect', methods=['POST'])
def detect():
    if random.random() < 0.5:
        # Old model
        return old_detector.detect(request.files['video'])
    else:
        # New model
        return new_detector.detect(request.files['video'])
```

## Maintenance

### Regular Tasks
- [ ] Review logs daily
- [ ] Monitor performance metrics
- [ ] Update dependencies monthly
- [ ] Security patches immediately
- [ ] Database optimization quarterly
- [ ] Disaster recovery drill monthly
- [ ] Capacity planning quarterly

### Incident Response

1. **Alert**: Notification received
2. **Triage**: Determine severity
3. **Mitigation**: Immediate action
4. **Resolution**: Fix root cause
5. **Post-Mortem**: Document learnings

