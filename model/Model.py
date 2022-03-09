from sqlalchemy.orm import backref
from social import db, bcrypt
import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(230), nullable = False, unique = True)
    fullname = db.Column(db.String(220), nullable= False)
    email  = db.Column(db.String(220), nullable= False, unique = True)
    password =db.Column(db.String(220), nullable = False)
    profile_picture  = db.Column(db.String(220), nullable= True, default = None)
    bio = db.Column(db.Text, nullable= True, default = None)
    created_at = db.Column(db.DateTime , nullable = False, default = datetime.datetime.utcnow())
    post_user = db.relationship('Post', foreign_keys  = 'Post.user_id',backref = 'user', lazy = 'dynamic')
    follower_id_user = db.relationship('Follow', foreign_keys = "Follow.follower_id", backref = 'follower', lazy = 'dynamic')
    following_id_user = db.relationship('Follow', foreign_keys = "Follow.following_id", backref = 'following', lazy = 'dynamic')
    post_like_user   =  db.relationship('Like', foreign_keys = 'Like.user_id', backref = 'post_like_user', lazy = 'dynamic')
    
    def hashpassword(self):
        self.password = bcrypt.generate_password_hash(self.password).decode('utf-8')
        
    def checkpassword(self,password):
        return bcrypt.check_password_hash(self.password,password)
    
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    image = db.Column(db.String(460), nullable = True)
    created_at = db.Column(db.DateTime , nullable = False, default = datetime.datetime.utcnow())
    post_like = db.relationship('Like', foreign_keys = 'Like.post_id', backref = 'likes', lazy = 'dynamic')
    
class Follow(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    follower_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    following_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    
    
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"),nullable = False)
    user_id = db.Column(db.Integer , db.ForeignKey("user.id"), nullable = False)
    
    
    
    
