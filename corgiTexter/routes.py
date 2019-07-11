import os
import secrets
from flask import flash, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image
from corgiTexter import app, bcrypt, db
from corgiTexter.forms import (LoginForm, PostForm, RegistrationForm,
                             UpdateAccountForm)
from corgiTexter.models import Post, User
from corgiTexter.twilioBackend import factPuller
from twilio.twiml.messaging_response import MessagingResponse
from corgiTexter.admin_portal import admin


@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', posts=posts, current_user=current_user)


@app.route('/about')
def about():
    corgi_file = url_for('static', filename='corgi.gif')
    return render_template('about.html', title='About', corgi_file=corgi_file)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
                                            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data.lower(),
                    password=hashed_pw)

        db.session.add(user)
        db.session.commit()

        flash('Your account has been  created you can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                                                    url_for('home'))
        else:
            flash('Login failed, please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profilePics',
                                picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    posts = Post.query.filter(Post.user_id == current_user.id)
    
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            if current_user.image_file != 'default.jpg':
                temp_image = current_user.image_file
                current_user.image_file = picture_file
                os.remove('corgiTexter/static/profilePics/' + temp_image)
            else:
                current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash('Your account has been updated successfully!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profilePics/' +
                         current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form, posts=posts, imageTest=current_user.image_file, user_id=current_user.id)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(fact=form.fact.data, source=form.source.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been added!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.fact = form.fact.data
        post.source = form.source.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.fact.data = post.fact
        form.source.data = post.source
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/account/<int:user_id>/delete_ap', methods=['POST'])
@login_required
def delete_account_posts(user_id):
    user = User.query.get_or_404(user_id)
    posts = user.posts
    for post in posts:
        db.session.delete(post)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/account/<int:user_id>/delete_a', methods=['POST'])
@login_required
def delete_account(user_id):
    user = User.query.get_or_404(user_id)
    posts = user.posts
    for post in posts:
        post.user_id = 9
        db.session.commit()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('home'))


## Connection for the HTTP GET request for Twilio
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    fact, source = factPuller()
    resp = MessagingResponse()
    resp.message("{} Source: {}".format(fact, source))
    return str(resp)
