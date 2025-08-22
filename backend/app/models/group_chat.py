from app.models.base_model import BaseModel
from app import db
from datetime import datetime

class GroupChat(BaseModel):
    __tablename__ = 'GroupChat'

    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey('GroupStudy.group_id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def to_dict(self):
        return {
            'message_id': self.message_id,
            'group_id': self.group_id,
            'sender_id': self.sender_id,
            'sender_name': self.sender.name if self.sender else None,
            'message': self.message,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None
        }
