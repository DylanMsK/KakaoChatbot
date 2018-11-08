from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    star = db.Column(db.Float, nullable=True)
    ratio = db.Column(db.Float, nullable=True)
    img = db.Column(db.String, nullable=True)
    
    def __init__(self, title, star, ratio, img):
        self.title = title
        self.star = star
        self.ratio = ratio
        self.img = img
    