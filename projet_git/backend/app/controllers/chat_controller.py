from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from flask_socketio import emit, join_room, leave_room
from app import db, socketio
from app.models import GlobalChat, GroupChat, GroupMembers

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/global', methods=['GET'])
@login_required
def get_global_messages():
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)

    messages = GlobalChat.query.order_by(GlobalChat.sent_at.desc()).offset(offset).limit(limit).all()
    messages.reverse()  # Show oldest first

    return jsonify({
        'messages': [msg.to_dict() for msg in messages]
    }), 200

@chat_bp.route('/global', methods=['POST'])
@login_required
def send_global_message():
    data = request.get_json()

    if not data.get('message') or not data['message'].strip():
        return jsonify({'error': 'Message cannot be empty'}), 400

    try:
        message = GlobalChat(
            sender_id=current_user.user_id,
            message=data['message'].strip()
        )
        message.save()

        # Emit to all connected clients
        socketio.emit('global_message', message.to_dict(), namespace='/')

        return jsonify({
            'message': 'Message sent successfully',
            'chat_message': message.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to send message'}), 500

@chat_bp.route('/group/<int:group_id>', methods=['GET'])
@login_required
def get_group_messages(group_id):
    # Check if user is a member of the group
    membership = GroupMembers.query.filter_by(
        group_id=group_id,
        user_id=current_user.user_id
    ).first()

    if not membership:
        return jsonify({'error': 'You are not a member of this group'}), 403

    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)

    messages = GroupChat.query.filter_by(group_id=group_id).order_by(
        GroupChat.sent_at.desc()
    ).offset(offset).limit(limit).all()
    messages.reverse()  # Show oldest first

    return jsonify({
        'messages': [msg.to_dict() for msg in messages]
    }), 200

@chat_bp.route('/group/<int:group_id>', methods=['POST'])
@login_required
def send_group_message(group_id):
    # Check if user is a member of the group
    membership = GroupMembers.query.filter_by(
        group_id=group_id,
        user_id=current_user.user_id
    ).first()

    if not membership:
        return jsonify({'error': 'You are not a member of this group'}), 403

    data = request.get_json()

    if not data.get('message') or not data['message'].strip():
        return jsonify({'error': 'Message cannot be empty'}), 400

    try:
        message = GroupChat(
            group_id=group_id,
            sender_id=current_user.user_id,
            message=data['message'].strip()
        )
        message.save()

        # Emit to group room
        socketio.emit('group_message', message.to_dict(), room=f'group_{group_id}')

        return jsonify({
            'message': 'Message sent successfully',
            'chat_message': message.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to send message'}), 500

# Socket.IO event handlers
@socketio.on('connect')
def on_connect():
    if current_user.is_authenticated:
        print(f"User {current_user.name} connected to chat")

@socketio.on('disconnect')
def on_disconnect():
    if current_user.is_authenticated:
        print(f"User {current_user.name} disconnected from chat")

@socketio.on('join_group')
def on_join_group(data):
    if current_user.is_authenticated:
        group_id = data.get('group_id')
        if group_id:
            # Verify user is a member of the group
            membership = GroupMembers.query.filter_by(
                group_id=group_id,
                user_id=current_user.user_id
            ).first()

            if membership:
                join_room(f'group_{group_id}')
                emit('status', {'msg': f'Joined group {group_id} chat'})

@socketio.on('leave_group')
def on_leave_group(data):
    if current_user.is_authenticated:
        group_id = data.get('group_id')
        if group_id:
            leave_room(f'group_{group_id}')
            emit('status', {'msg': f'Left group {group_id} chat'})
