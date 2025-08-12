from db import db

class User(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False)
    senha = db.Column(db.Text, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)