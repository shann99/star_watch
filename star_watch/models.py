from datetime import datetime
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
    profile_pic = db.Column(db.String(20), nullable=False, default='static/default.png')
    cards = db.relationship('Card', backref='user', lazy=True)
    
    def __repr__(self):
        return f"User('{self.id}','{self.name}','{self.email}','{self.profile_pic}')"

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    cover_image_src = db.Column(db.String(1000), nullable=False, default='/static/default-background.jpg')
    item_tags = db.Column(db.String(1000000))
    current_ep = db.Column(db.Integer, nullable=False, default=0)
    total_eps = db.Column(db.String(1000), nullable=False, default='0')
    description = db.Column(db.String(100000000))
    review = db.Column(db.String(100000000))
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Card('{self.id}','{self.title}','{self.date_added}','{self.user_id}')"