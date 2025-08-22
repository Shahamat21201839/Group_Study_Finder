from flask import Blueprint, request, jsonify, current_app as app
from flask_login import login_required, current_user
from app import db
from app.models import GroupStudy, GroupMembers, JoinRequest, Course, Notification, User
from datetime import datetime

group_bp = Blueprint('groups', __name__)

@group_bp.route('/', methods=['GET'])
@login_required
def get_groups():
    course_id = request.args.get('course_id')
    query = GroupStudy.query
    if course_id:
        query = query.filter_by(course_id=course_id)
    groups = query.all()
    return jsonify({'groups': [g.to_dict() for g in groups]}), 200

@group_bp.route('/my-groups', methods=['GET'])
@login_required
def get_my_groups():
    try:
        memberships = (
            db.session.query(GroupMembers, GroupStudy, Course)
            .join(GroupStudy, GroupMembers.group_id == GroupStudy.group_id)
            .join(Course, GroupStudy.course_id == Course.course_id)
            .filter(GroupMembers.user_id == current_user.user_id)
            .all()
        )
        groups = []
        for membership, group_study, course in memberships:
            member_count = GroupMembers.query.filter_by(group_id=group_study.group_id).count()
            group_data = group_study.to_dict()
            group_data['my_role'] = membership.role
            group_data['course'] = course.to_dict()
            group_data['members_count'] = member_count
            groups.append(group_data)
        return jsonify({'groups': groups}), 200
    except Exception:
        app.logger.exception("Failed to fetch my-groups")
        return jsonify({'error': 'Failed to fetch your groups'}), 500

@group_bp.route('/<int:group_id>', methods=['GET'])
@login_required
def get_group_detail(group_id):
    group = GroupStudy.query.get_or_404(group_id)
    members_query = (
        db.session.query(GroupMembers, User)
        .join(User, GroupMembers.user_id == User.user_id)
        .filter(GroupMembers.group_id == group_id)
        .all()
    )
    members, my_role = [], None
    for membership, user in members_query:
        user_dict = user.to_dict()
        user_dict['role'] = membership.role
        members.append(user_dict)
        if membership.user_id == current_user.user_id:
            my_role = membership.role
    has_pending_request = (
        JoinRequest.query
        .filter_by(group_id=group_id, user_id=current_user.user_id, status='pending')
        .first() is not None
    )
    group_data = group.to_dict()
    group_data.update({
        'members': members,
        'is_member': my_role is not None,
        'my_role': my_role,
        'has_pending_request': has_pending_request
    })
    return jsonify({'group': group_data}), 200

@group_bp.route('/', methods=['POST'])
@login_required
def create_group():
    data = request.get_json()
    for field in ['course_id', 'group_name', 'description']:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    course = Course.query.get(data['course_id'])
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    try:
        group = GroupStudy(
            course_id=data['course_id'],
            group_name=data['group_name'],
            description=data['description'],
            created_by=current_user.user_id
        )
        if data.get('session_start'):
            group.session_start = datetime.fromisoformat(data['session_start'])
        if data.get('session_end'):
            group.session_end = datetime.fromisoformat(data['session_end'])
        group.save()
        leader = GroupMembers(
            group_id=group.group_id,
            user_id=current_user.user_id,
            role='leader'
        )
        leader.save()
        return jsonify({'message': 'Group created', 'group': group.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to create group'}), 500

@group_bp.route('/<int:group_id>/join-request', methods=['POST'])
@login_required
def request_to_join(group_id):
    group = GroupStudy.query.get_or_404(group_id)
    if GroupMembers.query.filter_by(group_id=group_id, user_id=current_user.user_id).first():
        return jsonify({'error': 'Already a member'}), 400
    if JoinRequest.query.filter_by(group_id=group_id, user_id=current_user.user_id, status='pending').first():
        return jsonify({'error': 'Already requested'}), 400
    try:
        jr = JoinRequest(group_id=group_id, user_id=current_user.user_id)
        jr.save()
        leader_mem = GroupMembers.query.filter_by(group_id=group_id, role='leader').first()
        if leader_mem:
            Notification(
                user_id=leader_mem.user_id,
                message=f"{current_user.name} requested to join '{group.group_name}'"
            ).save()
        return jsonify({'message': 'Request sent'}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to send request'}), 500

@group_bp.route('/<int:group_id>/join-requests', methods=['GET'])
@login_required
def get_join_requests(group_id):
    if not GroupMembers.query.filter_by(group_id=group_id, user_id=current_user.user_id, role='leader').first():
        return jsonify({'error': 'Only leader can view requests'}), 403
    try:
        reqs = JoinRequest.query.filter_by(group_id=group_id, status='pending').all()
        return jsonify({'requests': [r.to_dict() for r in reqs]}), 200
    except Exception:
        app.logger.exception("Failed to fetch join requests")
        return jsonify({'error': 'Failed to fetch join requests'}), 500

@group_bp.route('/join-requests/<int:request_id>/respond', methods=['PUT'])
@login_required
def respond_to_join_request(request_id):
    jr = JoinRequest.query.get_or_404(request_id)
    data = request.get_json()
    if data.get('action') not in ['approve', 'reject']:
        return jsonify({'error': 'Invalid action'}), 400
    if not GroupMembers.query.filter_by(group_id=jr.group_id, user_id=current_user.user_id, role='leader').first():
        return jsonify({'error': 'Only leader can respond'}, ), 403
    try:
        if data['action'] == 'approve':
            jr.status = 'approved'
            jr.save()
            gm = GroupMembers(group_id=jr.group_id, user_id=jr.user_id, role='member')
            gm.save()
            Notification(user_id=jr.user_id,
                         message=f"Your request to join '{jr.group.group_name}' was approved"
            ).save()
        else:
            jr.status = 'rejected'
            jr.save()
            Notification(user_id=jr.user_id,
                         message=f"Your request to join '{jr.group.group_name}' was rejected"
            ).save()
        return jsonify({'message': f"Request {data['action']}d"}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to respond to request'}), 500

@group_bp.route('/<int:group_id>/leave', methods=['DELETE'])
@login_required
def leave_group(group_id):
    gm = GroupMembers.query.filter_by(group_id=group_id, user_id=current_user.user_id).first()
    if not gm:
        return jsonify({'error': 'Not a member'}), 400
    try:
        gm.delete()
        return jsonify({'message': 'Left group'}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to leave group'}), 500

@group_bp.route('/<int:group_id>/members/<int:user_id>', methods=['DELETE'])
@login_required
def kick_member(group_id, user_id):
    if not GroupMembers.query.filter_by(group_id=group_id, user_id=current_user.user_id, role='leader').first():
        return jsonify({'error': 'Only leader can remove members'}), 403
    gm = GroupMembers.query.filter_by(group_id=group_id, user_id=user_id).first()
    if not gm:
        return jsonify({'error': 'Member not found'}), 404
    try:
        gm.delete()
        return jsonify({'message': 'Member removed'}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to remove member'}), 500


