import os
import secrets
from flask import flash, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image
from core import app, bcrypt, db
from core.forms import (LoginForm, PostForm, RegistrationForm,
                             UpdateAccountForm)
from core.models import Post, User
import random
from core.admin_portal import admin
from twilio.twiml.messaging_response import MessagingResponse
from core.twilioBackend import factPuller


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(fact=form.fact.data, source=form.source.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been added!', 'success')
        return redirect(url_for('home'))
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', form=form, posts=posts, current_user=current_user)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
                                            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data.lower(),
                    password=hashed_pw, image_file='default_' + str(random.randrange(1, 4, 1)) + '.jpg')

        db.session.add(user)
        db.session.commit()

        #flash('Your account has been  created you can now login', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Registration', form=form)

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

@app.route('/termsofservice')
def tos():
    return render_template('tos.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post1/<int:post_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.fact.data = post.fact
        form.source.data = post.source
    return render_template('update_post.html', title='Update Post',
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



@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    posts = Post.query.filter(Post.user_id == current_user.id)
    
    form = UpdateAccountForm()

    if form.validate_on_submit():

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash('Your account has been updated successfully!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profilePics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form, posts=posts, user_id=current_user.id)


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