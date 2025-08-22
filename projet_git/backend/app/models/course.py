from app.models.base_model import BaseModel
from app import db

class Course(BaseModel):
    __tablename__ = 'Course'

    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String(10), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))

    # Relationships
    user_courses = db.relationship('UserCourses', backref='course', lazy='dynamic')
    group_studies = db.relationship('GroupStudy', backref='course', lazy='dynamic')
    course_feedback = db.relationship('CourseFeedback', backref='course', lazy='dynamic')

    def to_dict(self):
        return {
            'course_id': self.course_id,
            'course_code': self.course_code,
            'course_name': self.course_name,
            'instructor_id': self.instructor_id,
            'instructor_name': self.instructor.name if self.instructor else None
        }
