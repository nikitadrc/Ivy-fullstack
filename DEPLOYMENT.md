# Deployment Guide

This guide will help you deploy the AI Interview Chatbot application using Docker Compose.

## Prerequisites

1. Docker and Docker Compose installed on your system
2. OpenAI API key
3. Gmail account (for email notifications)
4. Domain name (optional, for production deployment)

## Deployment Steps

### 1. Environment Setup

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your actual values:
   - Set your OpenAI API key
   - Configure email settings
   - Set a strong JWT secret
   - Update database credentials if needed

### 2. Build and Run

1. Build and start all services:
   ```bash
   docker-compose up --build -d
   ```

2. Monitor the logs:
   ```bash
   docker-compose logs -f
   ```

### 3. Database Setup

The database migrations will run automatically when the backend container starts.

### 4. Verify Deployment

1. Frontend should be accessible at: `http://localhost:3000`
2. Backend API should be accessible at: `http://localhost:5000`

### 5. Production Deployment

For production deployment, additional steps are recommended:

1. Use HTTPS with SSL certificates
2. Set up a reverse proxy (e.g., Nginx)
3. Configure proper security headers
4. Set up monitoring and logging
5. Configure backups for the database

Example Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Frontend
    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api {
        proxy_pass http://backend:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 6. Maintenance

1. Update dependencies regularly
2. Monitor system resources
3. Back up the database periodically
4. Check logs for errors
5. Update SSL certificates before expiry

### 7. Scaling (Optional)

The application can be scaled horizontally:

1. Add more backend instances
2. Use a load balancer
3. Scale the database with replication
4. Implement caching strategies

### 8. Monitoring

Consider setting up:
1. Application monitoring (e.g., Prometheus + Grafana)
2. Error tracking (e.g., Sentry)
3. Log aggregation (e.g., ELK Stack)
4. Uptime monitoring

## Troubleshooting

Common issues and solutions:

1. Database connection issues:
   - Check if PostgreSQL container is running
   - Verify database credentials
   - Check network connectivity

2. Redis connection issues:
   - Verify Redis container is running
   - Check Redis connection string

3. Email sending issues:
   - Verify Gmail credentials
   - Check if less secure app access is enabled
   - Verify network connectivity

4. OpenAI API issues:
   - Check API key validity
   - Monitor API usage and limits
   - Check network connectivity

## Security Considerations

1. Keep environment variables secure
2. Regularly update dependencies
3. Use strong passwords
4. Implement rate limiting
5. Set up proper firewall rules
6. Regular security audits
7. Enable CORS properly
8. Implement proper authentication and authorization

## Backup Strategy

1. Database backups:
   ```bash
   docker-compose exec db pg_dump -U postgres interview_chatbot > backup.sql
   ```

2. Automated backup script included in `backup_and_cleanup.py`

## Support

For issues and support:
1. Check the troubleshooting guide
2. Review application logs
3. Check Docker container status
4. Verify environment variables 