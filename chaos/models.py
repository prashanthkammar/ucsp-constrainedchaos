from flask_login import UserMixin, current_user 
from werkzeug.security import generate_password_hash 

from .extensions import db, admin, ModelView 

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(50))
    password = db.Column(db.String(100)) 
    nextq = db.Column(db.Integer)
    present_try = db.Column(db.Integer)
    hint = db.Column(db.Integer)
    score = db.Column(db.Integer) 
    attempts = db.Column(db.String(5000))
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    is_admin = db.Column(db.Boolean)

    @property
    def unhashed_password(self):
        raise AttributeError('cannot view unhashed password!')
    
    def __repr__(self):
        return self.email 

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)

admin.add_view(MyModelView(User, db.session))