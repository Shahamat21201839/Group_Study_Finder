# Deployment Guide

## Production Deployment

### 1. Environment Setup
```bash
export FLASK_CONFIG=production
export DATABASE_URL="mysql+pymysql://user:pass@host:port/db"
export SECRET_KEY="your-secure-secret-key"
```

### 2. Frontend Build
```bash
cd frontend
npm run build
```

### 3. Backend Deployment
Use Gunicorn for production:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### 4. Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 5. Database Migration
```bash
flask db upgrade
```

### 6. SSL Setup
Use Let's Encrypt for free SSL certificates:
```bash
certbot --nginx -d your-domain.com
```
