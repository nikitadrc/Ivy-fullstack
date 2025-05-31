import pytest
from datetime import datetime, timedelta
from src.services.calendar_service import CalendarService
from src.services.email_service import EmailService
from src.services.storage_service import StorageService
from botocore.exceptions import ClientError

class TestCalendarService:
    def test_create_interview_event(self, mock_calendar_service, sample_interview_data):
        # Arrange
        event_data = {
            'summary': 'Interview Session',
            'start': {'dateTime': sample_interview_data['scheduled_time'].isoformat()},
            'end': {'dateTime': (sample_interview_data['scheduled_time'] + 
                               timedelta(minutes=sample_interview_data['duration_minutes'])).isoformat()}
        }
        mock_calendar_service.service.events().insert().execute.return_value = event_data

        # Act
        result = mock_calendar_service.create_interview_event(
            interviewer_email=sample_interview_data['interviewer_email'],
            candidate_email=sample_interview_data['candidate_email'],
            start_time=sample_interview_data['scheduled_time'],
            duration_minutes=sample_interview_data['duration_minutes']
        )

        # Assert
        assert result == event_data
        mock_calendar_service.service.events().insert.assert_called_once()

    def test_get_available_slots(self, mock_calendar_service, future_datetime):
        # Arrange
        mock_events = {
            'items': [
                {
                    'start': {'dateTime': future_datetime.isoformat()},
                    'end': {'dateTime': (future_datetime + timedelta(hours=1)).isoformat()}
                }
            ]
        }
        mock_calendar_service.service.events().list().execute.return_value = mock_events

        # Act
        slots = mock_calendar_service.get_available_slots(
            future_datetime,
            future_datetime + timedelta(days=1)
        )

        # Assert
        assert isinstance(slots, list)
        mock_calendar_service.service.events().list.assert_called_once()

class TestEmailService:
    def test_send_interview_scheduled(self, mock_email_service, sample_interview_data):
        # Act
        result = mock_email_service.send_interview_scheduled(
            to_email=sample_interview_data['candidate_email'],
            name=sample_interview_data['candidate_name'],
            date=sample_interview_data['scheduled_time'].strftime('%Y-%m-%d'),
            time=sample_interview_data['scheduled_time'].strftime('%H:%M'),
            meeting_link="https://meet.google.com/test"
        )

        # Assert
        assert result == {"status": "success"}
        mock_email_service.client.send.assert_called_once()

    def test_send_interview_reminder(self, mock_email_service, sample_interview_data):
        # Act
        result = mock_email_service.send_interview_reminder(
            to_email=sample_interview_data['candidate_email'],
            name=sample_interview_data['candidate_name'],
            time=sample_interview_data['scheduled_time'].strftime('%H:%M'),
            meeting_link="https://meet.google.com/test"
        )

        # Assert
        assert result == {"status": "success"}
        mock_email_service.client.send.assert_called_once()

class TestStorageService:
    def test_upload_file(self, mock_storage_service, temp_file):
        # Arrange
        with open(temp_file, 'rb') as f:
            mock_storage_service.s3_client.upload_fileobj.return_value = None
            mock_storage_service.generate_presigned_url.return_value = "https://test-url.com"

            # Act
            result = mock_storage_service.upload_file(f, "test.txt")

            # Assert
            assert 'file_path' in result
            assert 'url' in result
            assert result['url'] == "https://test-url.com"
            mock_storage_service.s3_client.upload_fileobj.assert_called_once()

    def test_download_file(self, mock_storage_service):
        # Arrange
        mock_body = b"Test content"
        mock_storage_service.s3_client.get_object.return_value = {'Body': mock_body}

        # Act
        result = mock_storage_service.download_file("test.txt")

        # Assert
        assert result == mock_body
        mock_storage_service.s3_client.get_object.assert_called_once()

    def test_delete_file(self, mock_storage_service):
        # Arrange
        mock_storage_service.s3_client.delete_object.return_value = None

        # Act
        result = mock_storage_service.delete_file("test.txt")

        # Assert
        assert result is True
        mock_storage_service.s3_client.delete_object.assert_called_once()

    def test_list_files(self, mock_storage_service):
        # Arrange
        mock_objects = {
            'Contents': [
                {
                    'Key': 'test.txt',
                    'Size': 100,
                    'LastModified': datetime.now()
                }
            ]
        }
        mock_storage_service.s3_client.list_objects_v2.return_value = mock_objects
        mock_storage_service.generate_presigned_url.return_value = "https://test-url.com"

        # Act
        result = mock_storage_service.list_files()

        # Assert
        assert len(result) == 1
        assert result[0]['key'] == 'test.txt'
        mock_storage_service.s3_client.list_objects_v2.assert_called_once() 