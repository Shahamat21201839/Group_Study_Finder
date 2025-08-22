from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Course, UserCourses
from werkzeug.security import generate_password_hash
import re

user_bp = Blueprint('users', __name__)

@user_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    data = request.get_json()

    try:
        # Update basic profile info
        if 'name' in data:
            current_user.name = data['name']

        if 'email' in data:
            # Validate email format
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, data['email']):
                return jsonify({'error': 'Invalid email format'}), 400

            # Check if email is already taken by another user
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.user_id != current_user.user_id:
                return jsonify({'error': 'Email already taken'}), 400

            current_user.email = data['email']

        current_user.save()
        return jsonify({
            'message': 'Profile updated successfully',
            'user': current_user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile'}), 500

@user_bp.route('/change-password', methods=['PUT'])
@login_required
def change_password():
    data = request.get_json()
    
    required_fields = ['current_password', 'new_password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Verify current password
    if not current_user.check_password(data['current_password']):
        return jsonify({'error': 'Current password is incorrect'}), 400
    
    # Validate new password length
    if len(data['new_password']) < 8:
        return jsonify({'error': 'New password must be at least 8 characters long'}), 400
    
    try:
        current_user.set_password(data['new_password'])
        current_user.save()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to change password'}), 500


@user_bp.route('/courses', methods=['GET'])
@login_required
def get_user_courses():
    # Return full course details for dropdown and profile lists
    doing = [uc.course.to_dict() for uc in current_user.user_courses if uc.status == 'doing']
    done  = [uc.course.to_dict() for uc in current_user.user_courses if uc.status == 'done']

    return jsonify({
        'doing': doing,
        'done': done
    }), 200

@user_bp.route('/courses', methods=['POST'])
@login_required
def add_user_course():
    data = request.get_json()

    if not data.get('course_id') or not data.get('status'):
        return jsonify({'error': 'Course ID and status are required'}), 400

    if data['status'] not in ['doing', 'done']:
        return jsonify({'error': 'Status must be either doing or done'}), 400

    # Check if course exists
    course = Course.query.get(data['course_id'])
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    # Check if user already has this course
    existing = UserCourses.query.filter_by(
        user_id=current_user.user_id,
        course_id=data['course_id']
    ).first()

    if existing:
        # Update existing status
        existing.status = data['status']
        existing.save()
        message = 'Course status updated successfully'
    else:
        # Add new course
        user_course = UserCourses(
            user_id=current_user.user_id,
            course_id=data['course_id'],
            status=data['status']
        )
        user_course.save()
        message = 'Course added successfully'

    return jsonify({'message': message}), 200

@user_bp.route('/courses/<int:course_id>', methods=['DELETE'])
@login_required
def remove_user_course(course_id):
    user_course = UserCourses.query.filter_by(
        user_id=current_user.user_id,
        course_id=course_id
    ).first()

    if not user_course:
        return jsonify({'error': 'Course not found in your list'}), 404

    try:
        user_course.delete()
        return jsonify({'message': 'Course removed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to remove course'}), 500

@user_bp.route('/search', methods=['GET'])
@login_required
def search_users():
    course_code = request.args.get('course_code')
    course_status = request.args.get('status')  # 'doing' or 'done'

    if not course_code:
        return jsonify({'error': 'Course code is required'}), 400

    # Find the course
    course = Course.query.filter_by(course_code=course_code).first()
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    # Build query for users with this course
    query = UserCourses.query.filter_by(course_id=course.course_id)

    if course_status and course_status in ['doing', 'done']:
        query = query.filter_by(status=course_status)

    user_courses = query.all()
    users = []

    for uc in user_courses:
        user_data = uc.user.to_dict()
        user_data['course_status'] = uc.status
        users.append(user_data)

    return jsonify({
        'course': course.to_dict(),
        'users': users
    }), 200
