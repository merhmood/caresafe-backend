from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class UserModel(db.Model):
    __tablename__ = 'user'
 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
 
    def __init__(self, name,age):
        self.name = name
        self.age = age
 
    def __repr__(self):
        return f"{self.name}:{self.age}"

class UserModel():
    __users__ = []
    
    def get_users(self):
        return self.__users__
    def add_user(self, user):
        self.__users__.append(user)