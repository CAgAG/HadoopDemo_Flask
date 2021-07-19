from app import db


class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'user: {self.username}'
