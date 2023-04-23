from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db


class Users(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String(200), nullable=False, unique=True)
    real_name = db.Column(db.String(200), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_type = db.Column(db.Enum('user', 'judge', 'admin', 'superadmin', 'athlete'), default='user')

class Category(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)

class Tournament(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    list_of_judges = db.relationship('Judge')
    list_of_athletes = db.relationship('Athlete')

class Judge(db.Model):
    __tablename__ = 'judge'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, unique=True, primary_key=True)
    user = db.relationship('Users', backref=db.backref('judge', uselist=False))
    category_name = db.Column(db.String(200), db.ForeignKey('category.name'), nullable=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=True)
    type_of_jury = db.Column(db.Enum('major', 'normal', default = 'normal'))


class Athlete(db.Model, UserMixin):
    __tablename__ = 'athlete'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, unique=True, primary_key=True)
    user = db.relationship('Users', backref=db.backref('athlete', uselist=False))
    category_type = db.Column(db.String(200), db.ForeignKey('category.name'), nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=True)
    list_of_poomsaes = db.relationship('Poomsae', secondary='athlete_poomsae')

    athlete_poomsae = db.Table('athlete_poomsae',
    db.Column('athlete_id', db.Integer, db.ForeignKey('athlete.id'), primary_key=True),
    db.Column('poomsae_id', db.Integer, db.ForeignKey('poomsae.id'), primary_key=True)
)


class Poomsae(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)


    @property
    def password(self):
        raise AttributeError('password is not a readable atribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<NAME %r>' % self.username
