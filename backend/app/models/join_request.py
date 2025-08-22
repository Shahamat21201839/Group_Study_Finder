from app.models.base_model import BaseModel
from app import db
from datetime import datetime

class JoinRequest(BaseModel):
    __tablename__ = 'JoinRequest'

    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey('GroupStudy.group_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
    status = db.Column(db.Enum('pending', 'approved', 'rejected', name='request_status'), default='pending')
    requested_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def to_dict(self):
        return {
            'request_id': self.request_id,
            'group_id': self.group_id,
            'group': self.group.to_dict() if self.group else None,
            'user_id': self.user_id,
            'user': self.user.to_dict() if self.user else None,
            'status': self.status,
            'requested_at': self.requested_at.isoformat() if self.requested_at else None
        }
