from flask import render_template, request, session, url_for, flash, redirect, get_flashed_messages
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import random
import re
from star_watch.models import User, Card
from star_watch import app, db


@app.route("/", methods=['GET','POST'])
@login_required
def index():
    watching = 'watching'
    item_list = Card.query.with_entities(Card.cover_image_src).all()
    images = [image[0] for image in item_list]
    

    random.shuffle(images)
   
    if request.method == "POST":
        media_image = request.form.get('add_image_form')
        tags = request.form.get('add_tags')
        title = request.form.get('add_title')
        current_ep = request.form.get('current_ep')
        total_eps = request.form.get('total_eps')
        description = request.form.get('description')
        rating = request.form.get('rating')
        status = request.form.get('status')

        card = Card(title=title, cover_image_src=media_image, item_tags=tags, current_ep=current_ep, total_eps=total_eps, status=status, description=description, rating=rating, user=current_user)
        db.session.add(card)
        db.session.commit()

        flash('Your new media has sucessfully been created', category="success")
        return redirect(url_for("index"))


    return render_template("index.html", user=current_user,  watch_status=watching, images=images)

@app.route("/planning", methods=['GET','POST'])
@login_required
def planning():
    if request.method == "POST":
        media_image = request.form.get('add_image_form')
        tags = request.form.get('add_tags')
        title = request.form.get('add_title')
        current_ep = request.form.get('current_ep')
        total_eps = request.form.get('total_eps')
        description = request.form.get('description')
        rating = request.form.get('rating')
        status = request.form.get('status')
        
        card = Card(title=title, cover_image_src=media_image, item_tags=tags, current_ep=current_ep, total_eps=total_eps,description=description, rating=rating, user=current_user)
        db.session.add(card)
        db.session.commit()
        
        
        planning = 'planning'

        flash('Your new media has sucessfully been created', category="success")
        return redirect(url_for("planning"))

    return render_template("planning.html", user=current_user)

@app.route("/paused", methods=['GET','POST'])
@login_required
def paused():
    if request.method == "POST":
        media_image = request.form.get('add_image_form')
        tags = request.form.get('add_tags')
        title = request.form.get('add_title')
        current_ep = request.form.get('current_ep')
        total_eps = request.form.get('total_eps')
        description = request.form.get('description')
        rating = request.form.get('rating')
        status = request.form.get('status')

        card = Card(title=title, cover_image_src=media_image, item_tags=tags, current_ep=current_ep, total_eps=total_eps, status=status, description=description, rating=rating, user=current_user)
        db.session.add(card)
        db.session.commit()
        
        
        paused = 'paused'

        flash('Your new media has sucessfully been created', category="success")
        return redirect(url_for("paused"))


    return render_template("paused.html", user=current_user)   

@app.route("/completed", methods=['GET','POST'])
@login_required
def completed():
    if request.method == "POST":
        media_image = request.form.get('add_image_form')
        tags = request.form.get('add_tags')
        title = request.form.get('add_title')
        current_ep = request.form.get('current_ep')
        total_eps = request.form.get('total_eps')
        description = request.form.get('description')
        rating = request.form.get('rating')

        card = Card(title=title, cover_image_src=media_image, item_tags=tags, current_ep=current_ep, total_eps=total_eps,description=description, rating=rating, user=current_user)
        db.session.add(card)
        db.session.commit()
        
        
        completed = 'completed'

        flash('Your new media has sucessfully been created', category="success")
        return redirect(url_for("completed"))

    return render_template("completed.html", user=current_user)

@app.route("/account", methods=['GET','POST'])
@login_required
def account_profile():
    return render_template("account.html", user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        else:
            email = request.form.get('login_address')
            password = request.form.get('login_pass')

            user = User.query.filter_by(email=email).first()

            if user:
                if check_password_hash(user.password, password):
                    flash("Logged in successfully!", category="success")
                    login_user(user, remember=False)
                    return redirect(url_for("index"))
                else:
                    flash("Incorrect password, please try again", category="error")
                    
            else:
                flash("Email does not exist", category="error")
            
    return render_template("login.html", user=current_user)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        else:
            email = request.form.get('email_address')
            name = request.form.get('name')
            password = request.form.get('pass_org')
            pass_confirm = request.form.get('pass_confirm')

            if password != pass_confirm:
                flash('Passwords must match, please try again', category='error') 
            
            user = User.query.filter_by(email=email).first()
            if user:
                flash("Email already exists", category="error")
            else:
                new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash("Account successfully created!", category="success")
                return redirect(url_for("index"))

    return render_template("signup.html", user=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out!", category="success")
    return redirect(url_for("login"))
    