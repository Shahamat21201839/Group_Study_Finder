from app.models.base_model import BaseModel
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(BaseModel, UserMixin):
    __tablename__ = 'User'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('student', 'teacher', name='user_role'), default='student')
    registered_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    # Relationships
    courses_teaching = db.relationship('Course', backref='instructor', lazy='dynamic')
    user_courses = db.relationship('UserCourses', backref='user', lazy='dynamic')
    created_groups = db.relationship('GroupStudy', backref='creator', lazy='dynamic')
    group_memberships = db.relationship('GroupMembers', backref='user', lazy='dynamic')
    join_requests = db.relationship('JoinRequest', backref='user', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    uploaded_materials = db.relationship('StudyMaterials', backref='uploader', lazy='dynamic')
    course_feedback = db.relationship('CourseFeedback', backref='user', lazy='dynamic')
    sent_global_messages = db.relationship('GlobalChat', backref='sender', lazy='dynamic')
    sent_group_messages = db.relationship('GroupChat', backref='sender', lazy='dynamic')

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_courses_doing(self):
        return [uc.course for uc in self.user_courses if uc.status == 'doing']

    def get_courses_done(self):
        return [uc.course for uc in self.user_courses if uc.status == 'done']

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'registered_at': self.registered_at.isoformat() if self.registered_at else None
        }
