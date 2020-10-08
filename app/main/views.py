from flask import Flask, render_template, redirect, url_for, abort, request
from . import main
from ..models import Posts, Comment, User, Subscribers
from .forms import CommentForm,PostForm,UpdateProfile
from flask_login import login_required, current_user
from ..import db, photos
from ..email import mail_message

 

@main.route('/',methods = ["GET", "POST"])
def index():
    posts = Posts.get_all_posts()
    
    user=User()
    if request.method == "POST":
        subscribed = Subscribers(email = request.form.get("subs"))
        db.session.add(subscribed)
        db.session.commit()

        mail_message("Welcome to The new blogsite", 
                        "email/welcome_user", subscribed.email)
       
    
    return render_template('index.html',posts = posts)

@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/post', methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = form.post.data
        owner_id = current_user
        title = form.title.data
        author = form.author.data
        new_post = Posts(owner_id =current_user._get_current_object().id,post=post,author=author,title=title)
        new_post.save_post()
        subs = Subscribers.query.all()
        for sub in subs:
            mail_message('New blog posted', 
                            "email/welcome_user", sub.email, new_post = new_post)
            pass

        return redirect(url_for('main.index'))
    return render_template('posts.html',form=form)

@main.route('/blog/<int:id>', methods = ['GET','POST'])
@login_required
def blog(id):
    post = Posts.query.filter_by(id = id).first()
  

    
    return render_template('blog.html',post=post)




@main.route('/comment/<int:post_id>', methods = ['GET','POST'])
@login_required
def new_comment(post_id):
    form = CommentForm()
    post=Posts.query.get(post_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(post=post,user_id = current_user._get_current_object().id, post_id = post_id)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('main.new_comment', post_id= post_id))
    all_comments = Comment.query.filter_by(post_id = post_id).all()
    return render_template('comment.html', form = form,comment = all_comments )

@main.route('/profile/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'images/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))