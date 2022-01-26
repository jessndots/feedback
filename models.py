
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

class User(db.Model):
    """User"""
    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)


    @classmethod
    def register(cls, first_name, last_name, email, username, pwd):
        """Register user w/ hashed password and return user"""

        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        return cls(first_name=first_name, last_name=last_name, email=email, username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that the user exists and password is correct. Return user if valid; else return False"""

        u = User.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False
        

class Feedback(db.Model):
    """Feedback"""
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.Text, db.ForeignKey('users.username', ondelete="CASCADE"))

    user = db.relationship('User', backref='feedback')