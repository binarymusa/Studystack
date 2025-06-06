from Stacks import db, login_manager,bcrypt 
from flask_login import UserMixin
from datetime import datetime, timedelta

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    user_role = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    topics = db.relationship('Topic', backref='author', lazy=True)
    role = db.relationship('Roles', backref='role', lazy=True)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    # check if a provided plain-text password matches the hashed password stored in the "password_hash" column
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Roles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    role_name = db.Column(db.String(length=30), nullable=False, unique=True)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cards = db.relationship('Card', backref='topic', lazy=True)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    last_reviewed = db.Column(db.DateTime)
    next_review = db.Column(db.DateTime)
    difficulty = db.Column(db.Integer, default=1)  # 1-5 scale
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)