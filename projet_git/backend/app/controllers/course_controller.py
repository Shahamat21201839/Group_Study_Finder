from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Course, User, CourseFeedback

course_bp = Blueprint('courses', __name__)

@course_bp.route('/', methods=['GET'])
@login_required
def get_courses():
    courses = Course.query.all()
    return jsonify({
        'courses': [course.to_dict() for course in courses]
    }), 200

@course_bp.route('/<int:course_id>', methods=['GET'])
@login_required
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return jsonify({'course': course.to_dict()}), 200

@course_bp.route('/', methods=['POST'])
@login_required
def create_course():
    # Only teachers can create courses
    if current_user.role != 'teacher':
        return jsonify({'error': 'Only teachers can create courses'}), 403

    data = request.get_json()

    if not all(k in data for k in ['course_code', 'course_name']):
        return jsonify({'error': 'Course code and name are required'}), 400

    # Check if course code already exists
    if Course.query.filter_by(course_code=data['course_code']).first():
        return jsonify({'error': 'Course code already exists'}), 400

    try:
        course = Course(
            course_code=data['course_code'],
            course_name=data['course_name'],
            instructor_id=current_user.user_id
        )
        course.save()

        return jsonify({
            'message': 'Course created successfully',
            'course': course.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create course'}), 500

@course_bp.route('/<int:course_id>/feedback', methods=['GET'])
@login_required
def get_course_feedback(course_id):
    course = Course.query.get_or_404(course_id)
    feedback_list = [fb.to_dict() for fb in course.course_feedback]

    # Calculate average rating
    ratings = [fb.rating for fb in course.course_feedback if fb.rating]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0

    return jsonify({
        'course': course.to_dict(),
        'feedback': feedback_list,
        'average_rating': round(avg_rating, 2),
        'total_feedback': len(feedback_list)
    }), 200

@course_bp.route('/<int:course_id>/feedback', methods=['POST'])
@login_required
def add_course_feedback(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.get_json()

    # Validate rating
    if not data.get('rating') or not (1 <= int(data['rating']) <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400

    # Check if user already gave feedback for this course
    existing_feedback = CourseFeedback.query.filter_by(
        course_id=course_id,
        user_id=current_user.user_id
    ).first()

    if existing_feedback:
        # Update existing feedback
        existing_feedback.rating = int(data['rating'])
        existing_feedback.comment = data.get('comment', '')
        existing_feedback.save()
        message = 'Feedback updated successfully'
    else:
        # Create new feedback
        feedback = CourseFeedback(
            course_id=course_id,
            user_id=current_user.user_id,
            rating=int(data['rating']),
            comment=data.get('comment', '')
        )
        feedback.save()
        message = 'Feedback added successfully'

    return jsonify({'message': message}), 200

@course_bp.route('/search', methods=['GET'])
@login_required
def search_courses():
    query = request.args.get('q', '')

    if len(query) < 2:
        return jsonify({'error': 'Search query must be at least 2 characters'}), 400

    courses = Course.query.filter(
        db.or_(
            Course.course_code.ilike(f'%{query}%'),
            Course.course_name.ilike(f'%{query}%')
        )
    ).all()

    return jsonify({
        'courses': [course.to_dict() for course in courses],
        'count': len(courses)
    }), 200
