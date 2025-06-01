from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from typing import List, Dict

class CalendarService:
    def __init__(self, credentials: Dict = None):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.credentials = credentials
        self.service = None
        if credentials:
            self._initialize_service()

    def _initialize_service(self):
        creds = Credentials.from_authorized_user_info(self.credentials, self.SCOPES)
        self.service = build('calendar', 'v3', credentials=creds)

    def create_interview_event(self, interviewer_email: str, candidate_email: str, 
                             start_time: datetime, duration_minutes: int = 60) -> Dict:
        if not self.service:
            raise ValueError("Calendar service not initialized")

        end_time = start_time + timedelta(minutes=duration_minutes)
        
        event = {
            'summary': 'Interview Session',
            'description': 'AI Interview Session',
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
            'attendees': [
                {'email': interviewer_email},
                {'email': candidate_email},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 30},
                ],
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': f"interview-{datetime.now().timestamp()}",
                    'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                }
            },
        }

        event = self.service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1,
            sendUpdates='all'
        ).execute()

        return event

    def get_available_slots(self, start_date: datetime, end_date: datetime) -> List[datetime]:
        if not self.service:
            raise ValueError("Calendar service not initialized")

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=start_date.isoformat() + 'Z',
            timeMax=end_date.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        
        # Convert events to busy times
        busy_times = []
        for event in events:
            start = datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date')))
            end = datetime.fromisoformat(event['end'].get('dateTime', event['end'].get('date')))
            busy_times.append((start, end))

        # Find available slots (assuming 1-hour slots)
        available_slots = []
        current = start_date
        while current < end_date:
            if current.hour < 9 or current.hour >= 17:  # Outside business hours
                current += timedelta(hours=1)
                continue

            is_available = True
            for busy_start, busy_end in busy_times:
                if current >= busy_start and current < busy_end:
                    is_available = False
                    break

            if is_available:
                available_slots.append(current)

            current += timedelta(hours=1)

        return available_slots

    def update_event(self, event_id: str, updated_event: Dict) -> Dict:
        if not self.service:
            raise ValueError("Calendar service not initialized")

        event = self.service.events().update(
            calendarId='primary',
            eventId=event_id,
            body=updated_event,
            sendUpdates='all'
        ).execute()

        return event

    def delete_event(self, event_id: str) -> None:
        if not self.service:
            raise ValueError("Calendar service not initialized")

        self.service.events().delete(
            calendarId='primary',
            eventId=event_id,
            sendUpdates='all'
        ).execute() 