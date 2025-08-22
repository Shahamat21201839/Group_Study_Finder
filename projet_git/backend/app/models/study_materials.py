from app.models.base_model import BaseModel
from app import db
from datetime import datetime

class StudyMaterials(BaseModel):
    __tablename__ = 'StudyMaterials'

    material_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey('GroupStudy.group_id'))
    title = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('User.user_id'))
    uploaded_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def to_dict(self):
        return {
            'material_id': self.material_id,
            'group_id': self.group_id,
            'title': self.title,
            'file_path': self.file_path,
            'uploaded_by': self.uploaded_by,
            'uploader_name': self.uploader.name if self.uploader else None,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }
