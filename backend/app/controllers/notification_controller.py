from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Notification, User, Course, UserCourses
from datetime import datetime, timedelta
import random

notification_bp = Blueprint('notifications', __name__)

@notification_bp.route('/', methods=['GET'])
@login_required
def get_notifications():
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'

    query = Notification.query.filter_by(user_id=current_user.user_id)

    if unread_only:
        query = query.filter_by(is_read=False)

    notifications = query.order_by(Notification.created_at.desc()).all()

    return jsonify({
        'notifications': [notification.to_dict() for notification in notifications],
        'unread_count': len([n for n in notifications if not n.is_read])
    }), 200

@notification_bp.route('/<int:notification_id>/mark-read', methods=['PUT'])
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.filter_by(
        notification_id=notification_id,
        user_id=current_user.user_id
    ).first()

    if not notification:
        return jsonify({'error': 'Notification not found'}), 404

    try:
        notification.mark_as_read()
        return jsonify({'message': 'Notification marked as read'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to mark notification as read'}), 500

@notification_bp.route('/mark-all-read', methods=['PUT'])
@login_required
def mark_all_notifications_read():
    try:
        notifications = Notification.query.filter_by(
            user_id=current_user.user_id,
            is_read=False
        ).all()

        for notification in notifications:
            notification.is_read = True

        db.session.commit()
        return jsonify({'message': f'Marked {len(notifications)} notifications as read'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to mark notifications as read'}), 500

@notification_bp.route('/generate-exam-notifications', methods=['POST'])
@login_required
def generate_exam_notifications():
    # This is a demo function to generate sample exam notifications
    # In a real application, this would be automated based on course schedules

    try:
        doing_courses = current_user.user_courses.filter_by(status='doing').all()

        if not doing_courses:
            return jsonify({'message': 'No ongoing courses found'}), 200

        notifications_created = 0

        for uc in doing_courses:
            # Generate random exam notifications for demonstration
            exam_types = ['Midterm', 'Final', 'Quiz', 'Assignment Due']
            exam_type = random.choice(exam_types)

            # Random date in the next 30 days
            days_ahead = random.randint(3, 30)
            exam_date = (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')

            message = f"Upcoming {exam_type} for {uc.course.course_name} ({uc.course.course_code}) on {exam_date}"

            notification = Notification(
                user_id=current_user.user_id,
                message=message
            )
            notification.save()
            notifications_created += 1

        return jsonify({
            'message': f'Generated {notifications_created} exam notifications',
            'notifications_created': notifications_created
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to generate notifications'}), 500

@notification_bp.route('/request-resources', methods=['POST'])
@login_required
def request_resources():
    data = request.get_json()

    if not data.get('course_id') or not data.get('resource_type'):
        return jsonify({'error': 'Course ID and resource type are required'}), 400

    course = Course.query.get(data['course_id'])
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    try:
        # Find users who have completed this course
        completed_users = UserCourses.query.filter_by(
            course_id=data['course_id'],
            status='done'
        ).all()

        if not completed_users:
            return jsonify({'message': 'No users found who have completed this course'}), 200

        notifications_sent = 0
        resource_type = data['resource_type']

        for uc in completed_users:
            if uc.user_id != current_user.user_id:  # Don't send to self
                message = f"{current_user.name} is requesting {resource_type} for {course.course_name} ({course.course_code}). Can you help?"

                notification = Notification(
                    user_id=uc.user_id,
                    message=message
                )
                notification.save()
                notifications_sent += 1

        return jsonify({
            'message': f'Resource request sent to {notifications_sent} users who completed this course',
            'notifications_sent': notifications_sent
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to send resource requests'}), 500
