# Deployment Guide

## Streamlit Cloud Deployment

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at streamlit.io)

### Steps

1. **Fork/Clone Repository**
   ```bash
   git clone https://github.com/Mangesh-Bhattacharya/cisco-network-topology-simulator.git
   ```

2. **Sign in to Streamlit Cloud**
   - Go to https://streamlit.io/cloud
   - Sign in with GitHub

3. **Deploy App**
   - Click "New app"
   - Select repository: `cisco-network-topology-simulator`
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Deploy"

4. **Configure Secrets** (if needed)
   - Go to App settings → Secrets
   - Add any API keys or credentials

5. **Access Your App**
   - Your app will be available at: `https://[your-app-name].streamlit.app`

## Docker Deployment

### Build and Run Locally

```bash
# Build image
docker build -t cisco-network-simulator .

# Run container
docker run -p 8501:8501 cisco-network-simulator

# Access at http://localhost:8501
```

### Deploy to Docker Hub

```bash
# Tag image
docker tag cisco-network-simulator:latest yourusername/cisco-network-simulator:latest

# Push to Docker Hub
docker push yourusername/cisco-network-simulator:latest
```

## AWS Deployment

### Using EC2

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04
   - Instance type: t2.medium or larger
   - Security group: Allow port 8501

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install -y python3-pip git
   git clone https://github.com/Mangesh-Bhattacharya/cisco-network-topology-simulator.git
   cd cisco-network-topology-simulator
   pip3 install -r requirements.txt
   ```

3. **Run Application**
   ```bash
   streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   ```

4. **Setup as Service** (optional)
   ```bash
   sudo nano /etc/systemd/system/cisco-simulator.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Cisco Network Simulator
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/cisco-network-topology-simulator
   ExecStart=/usr/local/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable and start:
   ```bash
   sudo systemctl enable cisco-simulator
   sudo systemctl start cisco-simulator
   ```

### Using ECS (Docker)

1. **Push to ECR**
   ```bash
   aws ecr create-repository --repository-name cisco-network-simulator
   docker tag cisco-network-simulator:latest [account-id].dkr.ecr.[region].amazonaws.com/cisco-network-simulator:latest
   docker push [account-id].dkr.ecr.[region].amazonaws.com/cisco-network-simulator:latest
   ```

2. **Create ECS Task Definition**
3. **Create ECS Service**
4. **Configure Load Balancer**

## Azure Deployment

### Using Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name cisco-simulator \
  --image yourusername/cisco-network-simulator:latest \
  --dns-name-label cisco-simulator \
  --ports 8501
```

## Google Cloud Deployment

### Using Cloud Run

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/[PROJECT-ID]/cisco-network-simulator

# Deploy to Cloud Run
gcloud run deploy cisco-simulator \
  --image gcr.io/[PROJECT-ID]/cisco-network-simulator \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Heroku Deployment

1. **Create Heroku App**
   ```bash
   heroku create cisco-network-simulator
   ```

2. **Add Procfile**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

## Environment Variables

Create `.env` file for sensitive data:

```env
# API Keys (if needed)
OPENAI_API_KEY=your_key_here
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here

# Database (if needed)
DATABASE_URL=postgresql://user:pass@host:5432/db

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
```

## SSL/HTTPS Setup

### Using Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

## Monitoring

### Health Check Endpoint

The app includes a health check at `/_stcore/health`

### Logging

Logs are written to stdout/stderr and can be collected using:
- CloudWatch (AWS)
- Stackdriver (GCP)
- Application Insights (Azure)

## Scaling

### Horizontal Scaling
- Use load balancer
- Deploy multiple instances
- Session state management required

### Vertical Scaling
- Increase instance size
- More CPU/RAM for larger topologies

## Backup and Recovery

- Regular database backups (if using database)
- Version control for code
- Export configurations regularly

## Security Checklist

- [ ] Enable HTTPS
- [ ] Set strong passwords
- [ ] Use environment variables for secrets
- [ ] Enable firewall rules
- [ ] Regular security updates
- [ ] Monitor access logs
- [ ] Implement rate limiting
- [ ] Use VPC/private networks

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   lsof -i :8501
   kill -9 [PID]
   ```

2. **Memory issues**
   - Increase instance size
   - Optimize code
   - Use caching

3. **Slow performance**
   - Enable caching
   - Optimize database queries
   - Use CDN for static assets

## Support

For deployment issues:
- GitHub Issues: https://github.com/Mangesh-Bhattacharya/cisco-network-topology-simulator/issues
- Email: mangesh.bhattacharya@ontariotechu.net
