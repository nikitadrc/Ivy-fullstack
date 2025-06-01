from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, List
from ..models import User, ProgressTrack, Message

class ProgressService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_progress(self, user_id: int) -> Dict:
        # Get all progress records for user
        progress_records = self.db.query(ProgressTrack).filter(
            ProgressTrack.user_id == user_id
        ).all()

        if not progress_records:
            return {
                "overall_progress": 0.0,
                "topic_progress": {},
                "recommendations": []
            }

        # Calculate topic-wise progress
        topic_progress = {}
        total_progress = 0.0
        for record in progress_records:
            topic_progress[record.topic] = record.progress
            total_progress += record.progress

        # Calculate overall progress
        overall_progress = total_progress / len(progress_records)

        # Generate recommendations
        recommendations = self.generate_recommendations(
            user_id,
            topic_progress
        )

        return {
            "overall_progress": overall_progress,
            "topic_progress": topic_progress,
            "recommendations": recommendations
        }

    def update_progress(
        self,
        user_id: int,
        topic: str,
        progress_increment: float = 0.1
    ) -> None:
        # Get or create progress record
        progress_record = self.db.query(ProgressTrack).filter(
            ProgressTrack.user_id == user_id,
            ProgressTrack.topic == topic
        ).first()

        if not progress_record:
            progress_record = ProgressTrack(
                user_id=user_id,
                topic=topic,
                progress=0.0
            )
            self.db.add(progress_record)

        # Update progress
        new_progress = min(1.0, progress_record.progress + progress_increment)
        progress_record.progress = new_progress
        progress_record.last_studied = datetime.utcnow()

        # Update streak
        self.update_streak(progress_record)

        self.db.commit()

    def update_streak(self, progress_record: ProgressTrack) -> None:
        today = datetime.utcnow().date()
        last_studied = progress_record.last_studied.date()

        if last_studied == today:
            return
        elif last_studied == today - timedelta(days=1):
            progress_record.streak_days += 1
        else:
            progress_record.streak_days = 1

    def get_study_streak(self, user_id: int) -> Dict:
        # Get the user's progress records
        progress_records = self.db.query(ProgressTrack).filter(
            ProgressTrack.user_id == user_id
        ).all()

        if not progress_records:
            return {
                "current_streak": 0,
                "longest_streak": 0,
                "last_study_date": None
            }

        # Find the most recent study date and current streak
        current_streak = max(record.streak_days for record in progress_records)
        last_study_date = max(record.last_studied for record in progress_records)

        return {
            "current_streak": current_streak,
            "longest_streak": current_streak,  # Implement proper longest streak tracking
            "last_study_date": last_study_date
        }

    def generate_recommendations(
        self,
        user_id: int,
        topic_progress: Dict[str, float]
    ) -> List[str]:
        # Find topics with low progress
        weak_topics = [
            topic for topic, progress in topic_progress.items()
            if progress < 0.6
        ]

        # Get recent messages to find topics the user has been studying
        recent_messages = self.db.query(Message).filter(
            Message.user_id == user_id,
            Message.timestamp > datetime.utcnow() - timedelta(days=7)
        ).all()

        recent_topics = set()
        for message in recent_messages:
            # Extract topics from messages (implement proper topic extraction)
            if message.content:
                # Simple keyword matching - improve this
                for topic in topic_progress.keys():
                    if topic.lower() in message.content.lower():
                        recent_topics.add(topic)

        # Prioritize weak topics that haven't been studied recently
        recommendations = [
            topic for topic in weak_topics
            if topic not in recent_topics
        ]

        return recommendations[:3]  # Return top 3 recommendations 