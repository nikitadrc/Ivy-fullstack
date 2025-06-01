# Free Alternative Services Setup Guide

## Calendar Integration
Instead of using Google Calendar API, we'll use a simple calendar event system that:
1. Stores events in the PostgreSQL database
2. Generates `.ics` files that users can download and import into their calendars
3. Sends email notifications for reminders

## Email Setup (Using Gmail)
1. Create a free Gmail account or use an existing one
2. Enable 2-Step Verification in your Google Account
3. Generate an App Password:
   - Go to Google Account settings
   - Search for "App Passwords"
   - Select "Mail" and your device
   - Copy the generated 16-character password
4. Set up environment variables:
   ```env
   EMAIL_USER=your.email@gmail.com
   EMAIL_APP_PASSWORD=your-16-char-app-password
   ```

Note: Gmail allows sending up to 500 emails per day for free.

## File Storage (Local Storage)
Instead of using AWS S3, we'll store files locally:

1. Create an uploads directory:
   ```bash
   mkdir uploads
   ```
2. The system will automatically store uploaded files in this directory
3. Files will be served directly from the backend server

### Backup Strategy
Since we're using local storage, it's important to regularly backup your data:
1. Set up regular backups of the `uploads` directory
2. Back up your PostgreSQL database regularly
3. Consider using `rsync` or similar tools for automated backups

## Environment Variables
Create a `.env` file with these variables:

```env
# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=interview_chatbot
DATABASE_URL=postgresql://postgres:postgres@db:5432/interview_chatbot

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Security
JWT_SECRET=your-secure-jwt-secret-here  # Generate a random string

# Email Configuration (Gmail)
EMAIL_SERVICE=gmail
EMAIL_USER=your.email@gmail.com
EMAIL_APP_PASSWORD=your-16-char-app-password

# Frontend Configuration
REACT_APP_API_URL=http://localhost:5000
```

## Security Notes
1. Keep your `.env` file secure and never commit it to version control
2. Regularly update your email password
3. Monitor your email sending limits
4. Keep your uploads directory properly secured
5. Set up regular backups of both your database and uploaded files 