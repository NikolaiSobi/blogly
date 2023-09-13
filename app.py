from flask import Flask, request, render_template, redirect, flash, session
from models import *


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()

connect_db(app)

@app.route('/')
def list_users():
    """Shows list of users in db"""
    users = User.query.all()
    return render_template('list.html', users=users)

@app.route('/', methods=['POST'])
def create_user():
    first_name = request.form['name1']
    last_name = request.form['name2']
    image_url = request.form['image']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f"/{new_user.id}")

@app.route('/edited<int:user_id>', methods=['POST'])
def edited(user_id):
    first_name = request.form['name1']
    last_name = request.form['name2']
    image_url = request.form['image']

    user = User.query.get(user_id)
    user.first_name = first_name if first_name else user.first_name
    user.last_name = last_name if last_name else user.last_name
    user.image_url = image_url if image_url else "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
    db.session.add(user)
    db.session.commit()
    return redirect(f"/{user.id}")



@app.route('/create')
def create_form():
    return render_template("create.html")

@app.route('/edit<int:user_id>')
def edit_user(user_id):
    user = User.query.get(user_id)
    return render_template('edit.html', user=user)

@app.route('/delete<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    User.query.filter_by(id = user_id).delete()
    db.session.commit()
    return redirect('/')


@app.route("/<int:user_id>")
def show_user(user_id):
    """Show details about single user"""
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)
