from models import *
from app import app

db.drop_all()
db.create_all()

joe = User(
    first_name = "Joe",
    last_name = "Smith",
    image_url = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")

bob = User(
    first_name = "Bob",
    last_name = "Smith",
    image_url = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")

db.session.add_all([joe, bob])
db.session.commit()

