from app.models.base_model import BaseModel
from app import db
from datetime import datetime

class GroupMembers(BaseModel):
    __tablename__ = 'GroupMembers'

    group_id = db.Column(db.Integer, db.ForeignKey('GroupStudy.group_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), primary_key=True)
    joined_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    role = db.Column(db.Enum('leader', 'member', name='member_role'), default='member')

    def to_dict(self):
        return {
            'group_id': self.group_id,
            'user_id': self.user_id,
            'user': self.user.to_dict() if self.user else None,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'role': self.role
        }
