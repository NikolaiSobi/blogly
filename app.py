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
    post_ids = Post.query.filter(Post.user_id == user_id).all()
    for i in range(len(post_ids)):
        postTags = PostTag.query.filter(PostTag.post_id == post_ids[i].id).all()
        for j in range(len(postTags)):
            db.session.delete(postTags[j])
            db.session.commit()
        post = Post.query.filter(Post.id == post_ids[i].id).first()
        db.session.delete(post)
        db.session.commit()
    User.query.filter_by(id = user_id).delete()
    db.session.commit()
    return redirect('/')


@app.route("/<int:user_id>")
def show_user(user_id):
    """Show details about single user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.get(user_id)
    post_all = Post.query.all()
    tag = Tag.query.get(user_id)
    tags_all = Tag.query.all()
    return render_template("details.html", user=user, posts=posts, post_all=post_all, tag=tag, tags_all=tags_all)

@app.route('/createPost<int:user_id>')
def create_post(user_id):
    user = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template('createPost.html', user=user, tags=tags)

@app.route('/addPost<int:user_id>', methods=['POST'])
def addPost(user_id):
    title = request.form['title']
    content = request.form['content']
    tag_list = request.form.getlist('checkbox')
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    for i in range(len(tag_list)):
        tag = Tag.query.filter(Tag.name == tag_list[i]).first()   
        postTag = PostTag(post_id=post.id, tag_id=tag.id)
        db.session.add(postTag)
        db.session.commit()


    return redirect(f'/{user_id}')

@app.route('/user<int:user_id>/post<int:post_id>')
def post_details(user_id, post_id):
    post = Post.query.get(post_id)
    postTags = Post.query.filter(Post.id == post_id).all()
    user = User.query.get(user_id)
    tags = PostTag.query.filter(PostTag.post_id == post_id).all()
    all_tags = []
    for i in range(len(tags)):
        tag = Tag.query.filter(Tag.id == tags[i].tag_id).first()
        all_tags.append(tag)

    return render_template('postDetails.html', post=post, user=user, postTags=postTags, tags=tags, all_tags=all_tags)

@app.route('/edit/user<int:user_id>/post<int:post_id>')
def editPost(user_id, post_id):
    user = User.query.get(user_id)
    post = Post.query.filter(Post.id == post_id).first()
    tags = Tag.query.all()

    return render_template('editPost.html', user=user, post=post, tags=tags)

@app.route('/delete/user<int:user_id>/<int:post_id>', methods=['POST'])
def deletePost(user_id, post_id):
    postTags = PostTag.query.filter(PostTag.post_id == post_id).all()
    for i in range(len(postTags)):
        db.session.delete(postTags[i])
    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()
    return redirect(f'/{user_id}')

@app.route('/editing/user<int:user_id>/post<int:post_id>', methods=['POST'])
def editing_post(user_id, post_id):
    post = Post.query.filter(Post.id == post_id).first()
    title = request.form['title']
    content = request.form['post']
    tag_list = request.form.getlist('checkbox')
    post.title = title if title else post.title
    post.content = content

    db.session.add(post)
    db.session.commit()

    postTags = PostTag.query.filter(PostTag.post_id == post_id).all()
    for i in postTags:
        db.session.delete(i)
        db.session.commit()

    for i in range(len(tag_list)):
        tag = Tag.query.filter(Tag.name == tag_list[i]).first()   
        postTag = PostTag(post_id=post.id, tag_id=tag.id)
        db.session.add(postTag)
        db.session.commit()
    

    return redirect(f'/{user_id}')

@app.route('/createTag')
def tag_list():
    tags = Tag.query.all()
    return render_template('tagList.html', tags=tags)

@app.route('/createdTag', methods=['POST'])
def created_tag():
    tag = request.form['name']
    tag = Tag(name=tag)

    db.session.add(tag)
    db.session.commit()

    return redirect('/')

@app.route('/tags/<tag_name>')
def edit_tag(tag_name):
    tag = Tag.query.filter(Tag.name == tag_name).first()
    postTag = PostTag.query.all()
    post = Post.query.all()
    return render_template('showTag.html', tag=tag, postTag=postTag, post=post)

@app.route('/edit<tag_name>')
def go_to(tag_name):
    tag = Tag.query.filter(Tag.name == tag_name).first()
    return render_template('editTag.html', tag=tag)

@app.route('/editedTag<tag_name>', methods=['POST'])
def edited_post(tag_name):
    tag = Tag.query.filter(Tag.name == tag_name).first()
    new_tag = request.form['name']
    tag.name = new_tag
    db.session.commit()
    return redirect('/')

@app.route('/delete<tag_name>')
def delete_tag(tag_name):
    tag = Tag.query.filter(Tag.name == tag_name).first()
    PostTag.query.filter(PostTag.tag_id == tag.id).delete()
    Tag.query.filter(Tag.name == tag_name).delete()
    
    db.session.commit()
    return redirect('/')
