from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(100), nullable=False)
    prompt = db.Column(db.String(500), nullable=False)
    response = db.Column(db.Text, nullable=False)
