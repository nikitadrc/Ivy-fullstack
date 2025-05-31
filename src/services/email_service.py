from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import List, Dict
import os
from jinja2 import Template

class EmailService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('SENDGRID_API_KEY')
        self.client = SendGridAPIClient(self.api_key)
        self.from_email = Email("noreply@aiinterviewer.com")

    def _get_template(self, template_name: str) -> Template:
        templates = {
            'interview_scheduled': """
                <h2>Interview Scheduled</h2>
                <p>Dear {{ name }},</p>
                <p>Your interview has been scheduled for {{ date }} at {{ time }}.</p>
                <p>Meeting link: {{ meeting_link }}</p>
                <p>Please ensure you:</p>
                <ul>
                    <li>Test your audio and video before the interview</li>
                    <li>Have a stable internet connection</li>
                    <li>Are in a quiet environment</li>
                </ul>
                <p>Best regards,<br>AI Interviewer Team</p>
            """,
            'interview_reminder': """
                <h2>Interview Reminder</h2>
                <p>Dear {{ name }},</p>
                <p>This is a reminder that your interview is scheduled for tomorrow at {{ time }}.</p>
                <p>Meeting link: {{ meeting_link }}</p>
                <p>Best regards,<br>AI Interviewer Team</p>
            """,
            'interview_feedback': """
                <h2>Interview Feedback</h2>
                <p>Dear {{ name }},</p>
                <p>Thank you for participating in the interview. Here is your feedback:</p>
                <div style="margin: 20px 0; padding: 20px; background-color: #f5f5f5;">
                    {{ feedback }}
                </div>
                <p>Best regards,<br>AI Interviewer Team</p>
            """
        }
        return Template(templates.get(template_name, ""))

    def send_interview_scheduled(self, to_email: str, name: str, date: str, 
                               time: str, meeting_link: str) -> Dict:
        template = self._get_template('interview_scheduled')
        html_content = template.render(
            name=name,
            date=date,
            time=time,
            meeting_link=meeting_link
        )

        message = Mail(
            from_email=self.from_email,
            to_emails=To(to_email),
            subject='Interview Scheduled - AI Interviewer',
            html_content=Content("text/html", html_content)
        )

        response = self.client.send(message)
        return response.to_dict()

    def send_interview_reminder(self, to_email: str, name: str, 
                              time: str, meeting_link: str) -> Dict:
        template = self._get_template('interview_reminder')
        html_content = template.render(
            name=name,
            time=time,
            meeting_link=meeting_link
        )

        message = Mail(
            from_email=self.from_email,
            to_emails=To(to_email),
            subject='Interview Reminder - Tomorrow',
            html_content=Content("text/html", html_content)
        )

        response = self.client.send(message)
        return response.to_dict()

    def send_interview_feedback(self, to_email: str, name: str, feedback: str) -> Dict:
        template = self._get_template('interview_feedback')
        html_content = template.render(
            name=name,
            feedback=feedback
        )

        message = Mail(
            from_email=self.from_email,
            to_emails=To(to_email),
            subject='Interview Feedback',
            html_content=Content("text/html", html_content)
        )

        response = self.client.send(message)
        return response.to_dict()

    def send_bulk_emails(self, to_emails: List[Dict], template_name: str, 
                        template_data: Dict) -> List[Dict]:
        template = self._get_template(template_name)
        responses = []

        for recipient in to_emails:
            html_content = template.render(**template_data, **recipient)
            
            message = Mail(
                from_email=self.from_email,
                to_emails=To(recipient['email']),
                subject=template_data.get('subject', 'AI Interviewer Notification'),
                html_content=Content("text/html", html_content)
            )

            response = self.client.send(message)
            responses.append(response.to_dict())

        return responses 