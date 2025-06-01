import pytest
from datetime import datetime, timedelta
from src.services.calendar_service import CalendarService
from src.services.email_service import EmailService
from src.services.storage_service import StorageService
from src.models.interview import Interview
from src.models.user import User

class TestInterviewFlow:
    def test_complete_interview_flow(self, db_session, mock_calendar_service, 
                                   mock_email_service, mock_storage_service, 
                                   sample_interview_data):
        # 1. Create users
        interviewer = User(
            email=sample_interview_data['interviewer_email'],
            name="Test Interviewer",
            role="interviewer"
        )
        candidate = User(
            email=sample_interview_data['candidate_email'],
            name=sample_interview_data['candidate_name'],
            role="candidate"
        )
        db_session.add_all([interviewer, candidate])
        db_session.commit()

        # 2. Schedule interview
        interview = Interview(
            candidate_id=candidate.id,
            interviewer_id=interviewer.id,
            position=sample_interview_data['position'],
            scheduled_time=sample_interview_data['scheduled_time'],
            duration_minutes=sample_interview_data['duration_minutes'],
            status="scheduled"
        )
        db_session.add(interview)
        db_session.commit()

        # 3. Create calendar event
        event_data = {
            'summary': 'Interview Session',
            'id': 'test_event_id',
            'hangoutLink': 'https://meet.google.com/test'
        }
        mock_calendar_service.service.events().insert().execute.return_value = event_data
        
        calendar_event = mock_calendar_service.create_interview_event(
            interviewer_email=interviewer.email,
            candidate_email=candidate.email,
            start_time=interview.scheduled_time,
            duration_minutes=interview.duration_minutes
        )
        
        interview.calendar_event_id = calendar_event['id']
        interview.meeting_link = calendar_event['hangoutLink']
        db_session.commit()

        # 4. Send email notifications
        notification_result = mock_email_service.send_interview_scheduled(
            to_email=candidate.email,
            name=candidate.name,
            date=interview.scheduled_time.strftime('%Y-%m-%d'),
            time=interview.scheduled_time.strftime('%H:%M'),
            meeting_link=interview.meeting_link
        )
        assert notification_result == {"status": "success"}

        # 5. Upload interview materials
        test_file_content = b"Test interview materials"
        mock_storage_service.s3_client.upload_fileobj.return_value = None
        mock_storage_service.generate_presigned_url.return_value = "https://test-url.com"

        file_info = mock_storage_service.upload_file(
            test_file_content,
            f"interview_{interview.id}_materials.pdf",
            content_type="application/pdf"
        )
        interview.materials_url = file_info['url']
        db_session.commit()

        # 6. Complete interview
        interview.status = "completed"
        interview.feedback = "Great interview performance"
        db_session.commit()

        # 7. Send feedback email
        feedback_result = mock_email_service.send_interview_feedback(
            to_email=candidate.email,
            name=candidate.name,
            feedback=interview.feedback
        )
        assert feedback_result == {"status": "success"}

        # Final assertions
        assert interview.status == "completed"
        assert interview.feedback is not None
        assert interview.materials_url is not None
        assert interview.meeting_link is not None
        assert interview.calendar_event_id is not None

class TestErrorHandling:
    def test_calendar_service_error(self, mock_calendar_service, sample_interview_data):
        mock_calendar_service.service.events().insert().execute.side_effect = Exception("Calendar API error")
        
        with pytest.raises(Exception) as exc_info:
            mock_calendar_service.create_interview_event(
                interviewer_email=sample_interview_data['interviewer_email'],
                candidate_email=sample_interview_data['candidate_email'],
                start_time=sample_interview_data['scheduled_time'],
                duration_minutes=sample_interview_data['duration_minutes']
            )
        assert "Calendar API error" in str(exc_info.value)

    def test_email_service_error(self, mock_email_service, sample_interview_data):
        mock_email_service.client.send.side_effect = Exception("Email sending failed")
        
        with pytest.raises(Exception) as exc_info:
            mock_email_service.send_interview_scheduled(
                to_email=sample_interview_data['candidate_email'],
                name=sample_interview_data['candidate_name'],
                date=sample_interview_data['scheduled_time'].strftime('%Y-%m-%d'),
                time=sample_interview_data['scheduled_time'].strftime('%H:%M'),
                meeting_link="https://meet.google.com/test"
            )
        assert "Email sending failed" in str(exc_info.value)

    def test_storage_service_error(self, mock_storage_service):
        mock_storage_service.s3_client.upload_fileobj.side_effect = Exception("Storage error")
        
        with pytest.raises(Exception) as exc_info:
            mock_storage_service.upload_file(
                b"test content",
                "test.txt"
            )
        assert "Storage error" in str(exc_info.value) 