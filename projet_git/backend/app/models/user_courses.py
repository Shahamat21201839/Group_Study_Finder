from app.models.base_model import BaseModel
from app import db

class UserCourses(BaseModel):
    __tablename__ = 'UserCourses'

    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'), primary_key=True)
    status = db.Column(db.Enum('doing', 'done', name='course_status'), nullable=False)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'course_id': self.course_id,
            'status': self.status,
            'course': self.course.to_dict() if self.course else None
        }
