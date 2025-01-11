from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'
    CORS(app)

    with app.app_context():
        from app.models import User
        from app.utils import initialize_recommender

        db.create_all()

        # Initialize the recommender and store it in app config
        app.config['recommender'] = initialize_recommender()

        # Register the blueprint
        from app.routes import routes_bp
        app.register_blueprint(routes_bp)

    return app

# Register user_loader
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
