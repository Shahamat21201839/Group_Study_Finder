from app.models.base_model import BaseModel
from app import db
from datetime import datetime

class CourseFeedback(BaseModel):
    __tablename__ = 'CourseFeedback'

    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
    rating = db.Column(db.Integer, db.CheckConstraint('rating >= 1 AND rating <= 5'))
    comment = db.Column(db.Text)
    submitted_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def to_dict(self):
        return {
            'feedback_id': self.feedback_id,
            'course_id': self.course_id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'rating': self.rating,
            'comment': self.comment,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None
        }
