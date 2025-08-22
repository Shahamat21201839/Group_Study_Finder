from app.models.base_model import BaseModel
from app import db
from datetime import datetime

class GroupStudy(BaseModel):
    __tablename__ = 'GroupStudy'

    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'), nullable=False)
    group_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('User.user_id'))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    session_start = db.Column(db.TIMESTAMP)
    session_end = db.Column(db.TIMESTAMP)

    # Relationships
    members = db.relationship('GroupMembers', backref='group', lazy='dynamic')
    join_requests = db.relationship('JoinRequest', backref='group', lazy='dynamic')
    study_materials = db.relationship('StudyMaterials', backref='group', lazy='dynamic')
    group_messages = db.relationship('GroupChat', backref='group', lazy='dynamic')

    def get_members_list(self):
        return [member.user for member in self.members]

    def get_leader(self):
        leader_membership = self.members.filter_by(role='leader').first()
        return leader_membership.user if leader_membership else None

    def to_dict(self):
        return {
            'group_id': self.group_id,
            'course_id': self.course_id,
            'course': self.course.to_dict() if self.course else None,
            'group_name': self.group_name,
            'description': self.description,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'session_start': self.session_start.isoformat() if self.session_start else None,
            'session_end': self.session_end.isoformat() if self.session_end else None,
            'members_count': self.members.count()
        }
