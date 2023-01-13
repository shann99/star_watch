from datetime import datetime
from sqlalchemy.sql import func
from flask_login import UserMixin
from star_watch import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150),nullable=False)
    password = db.Column(db.String(150),nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, server_default='/default.png')
    cards = db.relationship('Card', backref='user', lazy=True)
    
    def __repr__(self):
        return f"User('{self.id}','{self.name}','{self.email}','{self.profile_pic}')"

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.String(10000000), nullable=False, server_default='/background.jpg')
    item_tags = db.Column(db.String(1000000))
    current_ep = db.Column(db.Integer, nullable=False, default= 0)
    total_eps = db.Column(db.String(1000), nullable=False, server_default="0")
    description = db.Column(db.String(100000000))
    rating = db.Column(db.Integer)
    date_added = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    status = db.Column(db.String(1000), nullable=False, server_default="Planning")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Card('{self.id}','{self.title}','{self.date_added}','{self.image}','{self.user_id}')"