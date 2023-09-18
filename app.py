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
    user.image_url = image_url if image_url else user.image_url
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
    Post.query.filter_by(user_id = user_id).delete()
    User.query.filter_by(id = user_id).delete()
    db.session.commit()
    return redirect('/')


@app.route("/<int:user_id>")
def show_user(user_id):
    """Show details about single user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.get(user_id)
    post_all = Post.query.all()
    return render_template("details.html", user=user, posts=posts, post_all=post_all)

@app.route('/createPost<int:user_id>')
def create_post(user_id):
    user = User.query.get(user_id)
    return render_template('createPost.html', user=user)

@app.route('/addPost<int:user_id>', methods=['GET','POST'])
def addPost(user_id):
    title = request.form['title']
    content = request.form['content']
    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/{user_id}')

@app.route('/user<int:user_id>/post<int:post_id>')
def post_details(user_id, post_id):
    post = Post.query.get(post_id)
    user = User.query.get(user_id)

    return render_template('postDetails.html', post=post, user=user)

@app.route('/edit/user<int:user_id>/post<int:post_id>')
def editPost(user_id, post_id):
    user = User.query.get(user_id)
    post = Post.query.filter(Post.id == post_id).first()

    return render_template('editPost.html', user=user, post=post)

@app.route('/delete/user<int:user_id>/<int:post_id>', methods=['POST'])
def deletePost(user_id, post_id):
    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()
    return redirect(f'/{user_id}')

@app.route('/editing/user<int:user_id>/post<int:post_id>', methods=['POST'])
def editing_post(user_id, post_id):
    post = Post.query.filter(Post.id == post_id).first()
    title = request.form['title']
    content = request.form['post']

    post.title = title if title else post.title
    post.content = content
    db.session.add(post)
    db.session.commit()

    return redirect(f'/{user_id}')

