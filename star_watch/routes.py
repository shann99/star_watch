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
    #querying images where watch status equals watching
    item_list = Card.query.with_entities(Card.image).filter(Card.status=='Watching').all()
    #retrieving the image itself without the extra parenthesis and commas from the query list
    images = [image[0] for image in item_list]
    #remove image if it equals default background image so it's not put into the carousel
    for image in images:
        if image == 'static/default-background.jpg':
            images.remove(image)

    random.shuffle(images)
   
    if request.method == "POST":
        if request.form.get('add_image_form') != "":
            image = request.form.get('add_image_form')
        else:
            image = (url_for("static", filename="background.jpg"))
        tags = request.form.get('add_tags')
        title = request.form.get('add_title')
        if request.form.get('current_ep') != "":
            current_ep = request.form.get('current_ep')
        else: 
            current_ep = 0;
        if request.form.get('total_eps') != "":
            total_eps = request.form.get('total_eps')
        else: 
            total_eps = '?'
        description = request.form.get('description')
        rating = request.form.get('rating')
        status = request.form.get('status')

        card = Card(title=title, image=image, item_tags=tags, current_ep=current_ep, total_eps=total_eps, status=status, description=description, rating=rating, user=current_user)
        db.session.add(card)
        db.session.commit()

        flash('Your new media has sucessfully been added', category="success")
        return redirect(url_for("index"))

    return render_template("index.html", user=current_user, images=images)

@app.route("/planning", methods=['GET','POST'])
@login_required
def planning():
    if request.method == "POST":
        if request.form.get('add_image_form') != "":
            image = request.form.get('add_image_form')
        else:
            image = (url_for("static", filename="background.jpg"))
        tags = request.form.get('add_tags')
        title = request.form.get('add_title')
        if request.form.get('current_ep') != "":
            current_ep = request.form.get('current_ep')
        else: 
            current_ep = 0;
        if request.form.get('total_eps') != "":
            total_eps = request.form.get('total_eps')
        else: 
            total_eps = '?'
        description = request.form.get('description')
        rating = request.form.get('rating')
        status = request.form.get('status')

        card = Card(title=title, image=image, item_tags=tags, current_ep=current_ep, total_eps=total_eps, status=status, description=description, rating=rating, user=current_user)
        db.session.add(card)
        db.session.commit()
  
        flash('Your new media has sucessfully been added', category="success")
        return redirect(url_for("planning"))

    return render_template("planning.html", user=current_user)

@app.route("/paused", methods=['GET','POST'])
@login_required
def paused():
    if request.method == "POST":
        if request.form.get('add_image_form') != "":
            image = request.form.get('add_image_form')
        else:
            image = (url_for("static", filename="background.jpg"))
        tags = request.form.get('add_tags')
        title = request.form.get('add_title')
        if request.form.get('current_ep') != "":
            current_ep = request.form.get('current_ep')
        else: 
            current_ep = 0;
        if request.form.get('total_eps') != "":
            total_eps = request.form.get('total_eps')
        else: 
            total_eps = '?'
        description = request.form.get('description')
        rating = request.form.get('rating')
        status = request.form.get('status')

        card = Card(title=title, image=image, item_tags=tags, current_ep=current_ep, total_eps=total_eps, status=status, description=description, rating=rating, user=current_user)
        db.session.add(card)
        db.session.commit()
  
        flash('Your new media has sucessfully been added', category="success")
        return redirect(url_for("paused"))


    return render_template("paused.html", user=current_user)   

@app.route("/completed", methods=['GET','POST'])
@login_required
def completed():
    if request.method == "POST":
        if request.form.get('add_image_form') != "":
            image = request.form.get('add_image_form')
        else:
            image = (url_for("static", filename="background.jpg"))
        tags = request.form.get('add_tags')
        title = request.form.get('add_title')
        if request.form.get('current_ep') != "":
            current_ep = request.form.get('current_ep')
        else: 
            current_ep = 0;
        if request.form.get('total_eps') != "":
            total_eps = request.form.get('total_eps')
        else: 
            total_eps = '?'
        description = request.form.get('description')
        rating = request.form.get('rating')
        status = request.form.get('status')

        card = Card(title=title, image=image, item_tags=tags, current_ep=current_ep, total_eps=total_eps, status=status, description=description, rating=rating, user=current_user)
        db.session.add(card)
        db.session.commit()
  
        flash('Your new media has sucessfully been added', category="success")
        return redirect(url_for("completed"))


    return render_template("completed.html", user=current_user)



@app.route("/account", methods=['GET','POST'])
@login_required
def account_profile():
    if request.method == "POST":
        user = current_user;
        print(user.id)
        update_user = User.query.get(user.id)

        password = request.form.get("update_password")
        pass_confirm = request.form.get("update_password_confirm")
        
        if password != pass_confirm:
                flash('Passwords must match, please try again', category='error') 

        if request.form.get('update_profile_pic') != "":
            update_user.profile_pic = request.form.get('update_profile_pic')
        if request.form.get('update_email') != "":
            update_user.email = request.form.get('update_email')
        if request.form.get('update_name') != "":
            update_user.name = request.form.get('update_name')
        if request.form.get('update_password') != "":
            update_user.password = request.form.get('update_password')

        db.session.commit()
        success_message = "Your account has successfully been updated!"
        flash(success_message, category="info")
        return redirect(url_for("index"))
    return render_template("account.html", user=current_user)


@app.route("/edit/<int:card_id>/<card_title>", methods=['GET','POST'], strict_slashes=False)
@login_required
def editMedia(card_id, card_title):
    card = Card.query.get(card_id)
    if request.method == "POST":
        if request.form.get('edit_image_form') != "":
            card.image = request.form.get('edit_image_form')
        if request.form.get('edit_tags') != "":
            card.item_tags = request.form.get('edit_tags')
        if request.form.get('edit_title') != "":
            card.title = request.form.get('edit_title')
        if request.form.get('edit_current_ep') != "":
            card.current_ep = request.form.get('edit_current_ep')
        if request.form.get('edit_total_eps') != "":
            card.total_eps = request.form.get('edit_total_eps')
        if request.form.get('edit_description') != "":
            card.description = request.form.get('edit_description')
        if request.form.get('edit_rating') != "":
            card.rating = request.form.get('edit_rating')
        if request.form.get('edit_status') != "":
            card.status = request.form.get('edit_status')

        card.id = card_id 
        db.session.commit()
        success_message = f"{card.title} has successfully been updated!"
        flash(success_message, category="info")
        return redirect(url_for("index"))

    return render_template("edit.html",  user=current_user, card_id=card.id)

@app.route('/delete/<int:card_id>/<card_title>', methods=['POST'])
@login_required
def delete(card_id, card_title):
    card = Card.query.get(card_id)
    db.session.delete(card)
    db.session.commit()
    flash('Your media has been deleted', category="info")
    return redirect(url_for("index"))

#updating count with click of a button
@app.route('/update/<int:card_id>/<card_title>/<int:card_current_ep>', methods=['POST'])
@login_required
def update(card_id,card_title,card_current_ep):
    card = Card.query.get(card_id)
    print(card.current_ep)
    card.current_ep += 1;
    db.session.commit()
    return redirect(url_for("index"))


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
    