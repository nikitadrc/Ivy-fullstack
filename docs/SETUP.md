# AI Interview Chatbot Setup Guide

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Docker and Docker Compose
- PostgreSQL 14 (if running locally)
- Redis (if running locally)

## Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-interview-chatbot.git
cd ai-interview-chatbot
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory:
```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/interview_chatbot
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/interview_chatbot_test

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET=your_secure_jwt_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Google Calendar
GOOGLE_CALENDAR_CREDENTIALS={"web":{"client_id":"...","client_secret":"..."}}

# SendGrid
SENDGRID_API_KEY=your_sendgrid_api_key

# AWS
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name
```

5. Set up the frontend:
```bash
cd frontend-new
npm install
```

## Database Setup

1. Create the databases:
```bash
createdb interview_chatbot
createdb interview_chatbot_test
```

2. Run migrations:
```bash
flask db upgrade
```

## Running the Application

### Using Docker Compose (Recommended for Production)

1. Build and start the containers:
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- API Documentation: http://localhost:5000/docs

### Running Locally (Development)

1. Start the backend:
```bash
# In the root directory
flask run --debug
```

2. Start the frontend development server:
```bash
# In the frontend-new directory
npm run dev
```

3. Start Celery worker (for background tasks):
```bash
celery -A src.celery_worker.celery worker --loglevel=info
```

4. Start Flower (for monitoring Celery tasks):
```bash
celery -A src.celery_worker.celery flower
```

## Running Tests

1. Run backend tests:
```bash
pytest tests/
```

2. Run frontend tests:
```bash
cd frontend-new
npm test
```

3. Run with coverage:
```bash
pytest --cov=src tests/
```

## Development Tools

### Code Formatting

1. Format Python code:
```bash
black src/ tests/
```

2. Format TypeScript/JavaScript code:
```bash
cd frontend-new
npm run format
```

### Linting

1. Lint Python code:
```bash
flake8 src/ tests/
```

2. Lint TypeScript/JavaScript code:
```bash
cd frontend-new
npm run lint
```

### Type Checking

1. Check Python types:
```bash
mypy src/
```

2. Check TypeScript types:
```bash
cd frontend-new
npm run type-check
```

## Security Setup

1. Generate a secure JWT secret:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

2. Set up SSL/TLS certificates (Production):
```bash
# Using Let's Encrypt
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

3. Configure AWS IAM roles with minimal required permissions for S3 access.

4. Set up Google OAuth 2.0 credentials in the Google Cloud Console.

## Monitoring

1. Access Flower dashboard for Celery monitoring:
http://localhost:5555

2. Access PostgreSQL metrics:
http://localhost:9187

3. Access Redis metrics:
http://localhost:9121

## Troubleshooting

### Common Issues

1. Database connection errors:
- Check if PostgreSQL is running
- Verify database credentials in `.env`
- Ensure database exists

2. Redis connection errors:
- Check if Redis is running
- Verify Redis URL in `.env`

3. Frontend build issues:
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Clear build cache: `npm run clean`

### Getting Help

- Check the [FAQ](./FAQ.md)
- Open an issue on GitHub
- Contact the development team 