from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)



class User(db.Model):

    __tablename__ = "user"

    def __repr__(self):
        u = self
        return f"<user id={u.id}, first_name={u.first_name}, last_name={u.last_name}, img_url={u.image_url}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    image_url = db.Column(db.String(500))

