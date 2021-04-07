from flask_jwt import db

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return f"User ('{self.id}' ,'{self.public_id}', '{self.name}', '{self.password}', '{self.admin}' )"


class Authors(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),unique = True, nullable=False)
    book = db.Column(db.String(20),unique = True, nullable=False)
    country = db.Column(db.String(50),nullable=False)
    booker_prize = db.Column(db.Boolean)
    user_id = db.Column(db.Integer , nullable=False)

    def __repr__(self):
        return f"Author ('{self.id}' ,'{self.name}', '{self.book}', '{self.country}', '{self.booker_prize}', '{self.user_id}' )"


