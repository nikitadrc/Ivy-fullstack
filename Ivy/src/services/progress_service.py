from sqlalchemy.orm import Session
from typing import List, Dict, Any
from models import User, ProgressTrack, ChatSession
from datetime import datetime, timedelta

class ProgressService:
    def __init__(self, db: Session):
        self.db = db
        self.topic_weights = {
            "DSA": 0.3,
            "System Design": 0.3,
            "Technical Concepts": 0.2,
            "Behavioral": 0.1,
            "Coding Practice": 0.1
        }

    def update_progress(self, user_id: int, topic: str, progress_delta: float = 5.0) -> ProgressTrack:
        """Update progress for a specific topic"""
        progress = self.db.query(ProgressTrack).filter(
            ProgressTrack.user_id == user_id,
            ProgressTrack.topic == topic
        ).first()

        if progress:
            progress.progress_percentage = min(100.0, progress.progress_percentage + progress_delta)
            progress.last_updated = datetime.utcnow()
        else:
            progress = ProgressTrack(
                user_id=user_id,
                topic=topic,
                progress_percentage=progress_delta
            )
            self.db.add(progress)

        self.db.commit()
        self.db.refresh(progress)
        return progress

    def get_user_progress(self, user_id: int) -> Dict[str, float]:
        """Get progress for all topics for a user"""
        progress_tracks = self.db.query(ProgressTrack).filter(
            ProgressTrack.user_id == user_id
        ).all()

        progress = {track.topic: track.progress_percentage for track in progress_tracks}
        
        # Add missing topics with 0% progress
        for topic in self.topic_weights.keys():
            if topic not in progress:
                progress[topic] = 0.0

        return progress

    def get_overall_progress(self, user_id: int) -> float:
        """Calculate overall progress considering topic weights"""
        progress = self.get_user_progress(user_id)
        weighted_progress = sum(
            progress.get(topic, 0.0) * weight
            for topic, weight in self.topic_weights.items()
        )
        return weighted_progress

    def get_recommended_topics(self, user_id: int, limit: int = 3) -> List[Dict[str, Any]]:
        """Get recommended topics based on progress and recent activity"""
        progress = self.get_user_progress(user_id)
        
        # Get recent chat sessions
        recent_sessions = self.db.query(ChatSession).filter(
            ChatSession.user_id == user_id,
            ChatSession.created_at >= datetime.utcnow() - timedelta(days=7)
        ).all()
        
        # Calculate topic scores based on progress and recent activity
        topic_scores = {}
        for topic, percentage in progress.items():
            # Lower progress means higher priority
            progress_score = 100 - percentage
            
            # Check recent activity
            recent_activity = sum(
                1 for session in recent_sessions
                if any(topic.lower() in str(msg).lower() 
                      for msg in session.chat_history)
            )
            
            # Combine scores (progress_score + recency_bonus + weight_bonus)
            topic_scores[topic] = (
                progress_score +
                (recent_activity * 10) +  # Bonus for recent activity
                (self.topic_weights.get(topic, 0) * 100)  # Weight bonus
            )
        
        # Sort topics by score and return top recommendations
        sorted_topics = sorted(
            topic_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {
                "topic": topic,
                "current_progress": progress[topic],
                "priority": "High" if score > 150 else "Medium" if score > 100 else "Low"
            }
            for topic, score in sorted_topics[:limit]
        ]

    def get_study_streak(self, user_id: int) -> int:
        """Calculate the user's current study streak in days"""
        sessions = self.db.query(ChatSession.created_at).filter(
            ChatSession.user_id == user_id
        ).order_by(ChatSession.created_at.desc()).all()
        
        if not sessions:
            return 0
            
        streak = 0
        current_date = datetime.utcnow().date()
        
        for i, (session_date,) in enumerate(sessions):
            session_date = session_date.date()
            if i == 0 and (current_date - session_date).days > 1:
                break
            elif i > 0 and (prev_date - session_date).days > 1:
                break
            
            if i == 0 or session_date != prev_date:
                streak += 1
            
            prev_date = session_date
            
        return streak 