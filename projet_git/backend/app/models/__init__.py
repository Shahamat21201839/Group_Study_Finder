# Import all models to make them available
from .base_model import BaseModel
from .user import User
from .course import Course
from .user_courses import UserCourses
from .group_study import GroupStudy
from .group_members import GroupMembers
from .join_request import JoinRequest
from .notification import Notification
from .study_materials import StudyMaterials
from .course_feedback import CourseFeedback
from .global_chat import GlobalChat
from .group_chat import GroupChat

# Make all models available for import
__all__ = [
    'BaseModel', 'User', 'Course', 'UserCourses', 'GroupStudy', 
    'GroupMembers', 'JoinRequest', 'Notification', 'StudyMaterials',
    'CourseFeedback', 'GlobalChat', 'GroupChat'
]
