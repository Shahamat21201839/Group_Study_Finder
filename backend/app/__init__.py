from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_socketio import SocketIO
from config import config
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
socketio = SocketIO()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.url_map.strict_slashes = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    CORS(
        app,
        resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}},
        supports_credentials=True
    )

    # Initialize SocketIO with proper CORS
    socketio.init_app(
        app,
        cors_allowed_origins=app.config['CORS_ORIGINS'],
        async_mode='threading',
        logger=True,
        engineio_logger=True
    )

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    # Register blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.user_controller import user_bp
    from app.controllers.course_controller import course_bp
    from app.controllers.group_controller import group_bp
    from app.controllers.chat_controller import chat_bp
    from app.controllers.notification_controller import notification_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(course_bp, url_prefix='/api/courses')
    app.register_blueprint(group_bp, url_prefix='/api/groups')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')

    @app.errorhandler(Exception)
    def handle_all_errors(err):
        code = getattr(err, 'code', 500)
        message = getattr(err, 'description', str(err))
        response = jsonify({'error': message})
        response.status_code = code
        return response

    upload_dir = app.config.get('UPLOAD_FOLDER')
    if upload_dir and not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    return app


