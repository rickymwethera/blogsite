from . import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255),unique = True,nullable = False)
    email = db.Column(db.String(255),unique = True,nullable = False)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password = db.Column(db.String(255),nullable = False)
    pass_secure = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.username}'

class Posts(db.Model):
    __tablename__= 'posts'
    id = db.Column(db.Integer,primary_key = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    author = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime, default=db.func.current_timestamp())
    title = db.Column(db.String(50))
    post = db.Column(db.String(999))
    

    comments = db.relationship('Comment',backref='post',lazy='dynamic')
   
    def save_post(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_posts(cls):
        return Posts.query.order_by(Posts.date_posted).all()

    def delete_post(self):
        db.session.delete(self)
        db.session.commit()

    
    def __repr__(self):
        return f'User {self.pitch}'

class Comment(db.Model):
    __tablename__='comments'
    
    id = db.Column(db.Integer,primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    description = db.Column(db.Text)

    
    def __repr__(self):
        return f"Comment : id: {self.id} comment: {self.description}"


class Subscribers(db.Model):
    __tablename__ = "subscribers"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), unique = True, index = True)

