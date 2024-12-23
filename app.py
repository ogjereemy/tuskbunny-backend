from flask import Flask
from db import db
from flask_jwt_extended import JWTManager
from config import Config
from flask_migrate import Migrate
from models import User, Task, Bid, Category, Review, Payment, Notification


app = Flask(__name__)
app.config.from_object(Config)

# Extensions
db.init_app(app)       # Initialize the app with SQLAlchemy
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Database migration
@app.before_request
def create_tables():
    db.drop_all()
    db.create_all()


# Import routes
from routes.auth import auth_bp
from routes.task import task_bp
from routes.review import review_bp
from routes.payment import payment_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(task_bp, url_prefix='/tasks')
app.register_blueprint(review_bp, url_prefix='/reviews')
app.register_blueprint(payment_bp, url_prefix='/payments')



if __name__ == '__main__':
    app.run(debug=True)
