from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__= 'users'
    
    id =db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    pitch = db.relationship('Pitch',backref = 'users',lazy="dynamic")
    comment = db.relationship('Comment', backref ='comments',lazy ="dynamic")
    votes = db.relationship('Vote',backref ='users',lazy ="dynamic")
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

            

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

            
    
    def __repr__(self):
        return f'User {self.username}'
    
class Pitch(db.Model):
    __tablename__='pitch'
    
    id = db.Column(db.Integer,primary_key = True)
    content =  db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    title = db.Column(db.String(255))
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    comments = db.relationship('Comment',backref = 'pitches', lazy ="dynamic")
    votes = db.relationship('Vote', backref = 'pitches', lazy = "dynamic")
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    
    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_pitches(cls):
        Pitch.all_pitches.clear()

    # display pitches

    def get_pitches(id):
        pitches = Pitch.query.filter_by(category=id).all()
        return pitches

    
    
    def __repr__(self):
        return f'Pitch {self.pitch_id}'
    
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    pitch = db.relationship('Pitch',backref = 'categories', lazy ="dynamic")
    
    def save_category(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_categories(cls):
        category = Category.query.all()
        return category 
    
    def __repr__(self):
        return f'Category {self.id}'
    
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key = True)
    feedback = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitch.id'))
    votes = db.relationship('Vote', backref = 'comments', lazy = "dynamic")

    def save_comment(self):
        '''
        Function that saves comments
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(self, id):
        comment = Comments.query.order_by(Comments.time_posted.desc()).filter_by(pitches_id=id).all()
        return comment
class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key = True)
    vote = db.Column(db.Integer)
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitch.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def save_vote(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_votes(cls,user_id,pitch_id):
        votes = Vote.query.filter_by(user_id=user_id, pitches_id=pitch_id).all()
        return votes       
    
# class Comment(db.model):
#     __tablename__='comment'
    
# class Category(db.model):
          