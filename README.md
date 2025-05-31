# AI Interview Chatbot

An intelligent chatbot platform for conducting automated technical interviews, powered by AI.

## Features

- User authentication and authorization
- Interview scheduling and management
- Real-time chat interface with AI interviewer
- File upload and management
- Calendar integration (Google Calendar)
- Email notifications (SendGrid)
- File storage (AWS S3)

## Tech Stack

### Backend
- FastAPI (Python web framework)
- PostgreSQL (Database)
- Redis (Caching and session management)
- SQLAlchemy (ORM)
- Alembic (Database migrations)
- pytest (Testing)

### Frontend
- React with TypeScript
- Material-UI components
- React Query for API integration
- Jest and React Testing Library
- WebSocket for real-time chat

### Infrastructure
- Docker and Docker Compose
- GitHub Actions (CI/CD)
- AWS S3 for file storage
- Nginx as reverse proxy

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- Docker and Docker Compose
- PostgreSQL 13+
- Redis

### Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-interview-chatbot.git
cd ai-interview-chatbot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install backend dependencies:
```bash
pip install -r requirements.txt
```

4. Install frontend dependencies:
```bash
cd frontend
npm install
```

5. Set up environment variables:
```bash
# Backend (.env)
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=interview_bot
JWT_SECRET=your_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
SENDGRID_API_KEY=your_sendgrid_key
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_BUCKET_NAME=your_bucket_name

# Frontend (.env.local)
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
```

### Database Setup

1. Create the database:
```bash
createdb interview_bot
```

2. Run database migrations:
```bash
alembic upgrade head
```

### Running the Application

#### Using Docker Compose (Recommended)

```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs

#### Manual Development Setup

1. Start the backend server:
```bash
uvicorn src.main:app --reload --port 8000
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

## Testing

### Backend Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src tests/
```

### Frontend Tests

```bash
cd frontend
npm test

# Run with coverage
npm test -- --coverage
```

## API Documentation

The API documentation is available at:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Deployment

### Production Setup

1. Update the production configurations in `docker-compose.prod.yml`
2. Set up SSL certificates
3. Configure environment variables for production
4. Deploy using Docker Compose:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Monitoring and Logging

- Application logs are available in Docker logs
- Monitoring is set up using Prometheus and Grafana
- Error tracking is configured with Sentry

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security

- All endpoints are protected with JWT authentication
- Passwords are hashed using bcrypt
- API keys and secrets are stored in environment variables
- CORS is configured for security
- Rate limiting is implemented on sensitive endpoints

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 